import os
import stat
import uuid
from pathlib import Path
from time import sleep
from typing import Optional, List, Dict, Tuple

import paramiko
import typer
from paramiko.client import SSHClient
from paramiko.config import SSHConfig
from paramiko.hostkeys import HostKeys
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_client import SFTPClient
from thestage_core.entities.file_item import FileItemEntity
from thestage_core.services.filesystem_service import FileSystemServiceCore

from thestage.exceptions.remote_server_exception import RemoteServerException
from thestage.helpers.logger.app_logger import app_logger
from thestage.entities.enums.shell_type import ShellType
from thestage.i18n.translation import __
from thestage.services.clients.thestage_api.dtos.sftp_path_helper import SftpPathHelper, SftpFileItemEntity

old_value: int = 0


class RemoteServerService(object):

    def __init__(
            self,
            file_system_service: FileSystemServiceCore,
    ):
        self.__file_system_service = file_system_service

    def __get_client(
            self,
            ip_address: str,
            username: str,
    ) -> Optional[SSHClient]:
        config_by_ip = None
        ssh_path = self.__file_system_service.get_ssh_path()
        ssh_config_path = ssh_path.joinpath('config')
        #ssh_config_path = Path('~/.ssh/config')
        config_path = ssh_config_path.expanduser()
        if config_path.exists():
            config = SSHConfig.from_path(config_path)
            config_by_ip = config.lookup(ip_address)
        client = SSHClient()
        try:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if config_by_ip:
                key_file_name = config_by_ip['identityfile'][0] if config_by_ip and 'identityfile' in config_by_ip and len(config_by_ip['identityfile']) > 0 else None
                client.connect(
                    hostname=ip_address,
                    username=username,
                    timeout=60,
                    allow_agent=False if key_file_name else True,
                    look_for_keys=False if key_file_name else True,
                    key_filename=key_file_name.replace('.pub', '') if key_file_name else None,
                )
            else:
                client.connect(
                    hostname=ip_address,
                    username=username,
                    timeout=60,
                )
            return client

        except Exception as ex:
            if client:
                client.close()
                typer.echo(f"Error connecting to {ip_address} as {username} ({ex})")
            app_logger.error(f"Error connecting to {ip_address} as {username} ({ex})")
            raise RemoteServerException(
                message=__("Unable to connect to remote server"),
                ip_address=ip_address,
                username=username,
            )

    @staticmethod
    def is_shell_present(
            lines: List[str],
    ) -> Optional[ShellType]:
        bash_present, sh_present = False, False
        for line in lines:
            if 'bin/bash' in line:
                bash_present = True
                break
            elif 'bin/sh' in line:
                sh_present = True

        if bash_present:
            return ShellType.BASH
        if sh_present:
            return ShellType.SH
        else:
            return None

    def get_shell_from_container(
            self,
            ip_address: str,
            username: str,
            docker_name: str,
    ) -> Optional[ShellType]:
        client: Optional[SSHClient] = self.__get_client(ip_address=ip_address, username=username)
        stdin, stdout, stderr = client.exec_command(f'docker exec -it {docker_name} cat /etc/shells', get_pty=True)
        shell = self.is_shell_present(lines=stdout.readlines())
        client.close()

        return shell

    def check_if_host_in_list_known(self, ip_address: str) -> bool:
        try:
            #os.system(f"ssh-keygen -F 34.198.189.175")
            ssh_path = self.__file_system_service.get_ssh_path()
            known_host_path = ssh_path.joinpath('known_hosts')
            if known_host_path.exists():
                host_keys = HostKeys(filename=str(known_host_path.absolute()))
                result = host_keys.lookup(ip_address)
                if result is not None:
                    return True
                else:
                    return False
        except Exception as ex:
            raise FileNotFoundError(f"Error reading SSH known hosts file: {ex}")
        return False

    def connect_to_instance(
            self,
            ip_address: str,
            username: str,
    ):
        try:
            os.system(f"ssh {username}@{ip_address}")
        except Exception as ex:
            app_logger.error(f"Error connecting to {ip_address} as {username} ({ex})")
            raise RemoteServerException(
                message=__("Unable to connect to remote server"),
                ip_address=ip_address,
                username=username,
            )

    def connect_to_container(
            self,
            ip_address: str,
            username: str,
            docker_name: str,
            shell: ShellType
    ):
        try:
            os.system(f"ssh -tt {username}@{ip_address} 'docker exec -it {docker_name} {shell.value}'")
        except Exception as ex:
            app_logger.exception(f"Error connecting to {ip_address} as {username} ({ex})")
            raise RemoteServerException(
                message=__("Unable to connect to remote server"),
                ip_address=ip_address,
                username=username,
            )

    @staticmethod
    def find_path_mapping(
            directory_mapping: Dict[str, str],
            destination_path: Optional[str] = None,
    ) -> Optional[str]:

        template = destination_path if destination_path else '/public'

        if not directory_mapping:
            typer.echo(__("Mapping folders not found"))
            raise typer.Exit(1)

        for key, value in directory_mapping.items():
            if value == template:
                return key
        return None

    @staticmethod
    def check_path_mapping(
            directory_mapping: Dict[str, str],
            path: Optional[str],
            is_upload: bool = True,
            is_folder: bool = False,
    ) -> Optional[SftpPathHelper]:
        if not directory_mapping:
            typer.echo(__("Mapping folders not found"))
            raise typer.Exit(1)

        public_src, public_desc = None, None

        for key, value in directory_mapping.items():
            #template = value if is_upload else key
            template = value

            if value == '/public':
                #public_src = key if is_upload else value
                #public_desc = value if is_upload else key
                public_src = value
                public_desc = key

            if template in path:
                path_list = path.split('/')
                return SftpPathHelper(
                    tmp_container_path='/'.join(path_list[0:-1]),
                    tmp_instance_path='/'.join(path.replace(template, key).split('/')[0:-1]),
                    item_name=path_list[-1],
                )

        if public_src == None:
            typer.echo(__("Public folder not found"))
            raise typer.Exit(1)

        tmp_folder = f"{uuid.uuid4()}"
        path_list = path.split('/')
        last = path_list[-1]

        return SftpPathHelper(
            tmp_container_path=f"{public_src}/{tmp_folder}",
            tmp_instance_path=f"{public_desc}/{tmp_folder}",
            tmp_folder_path=f"{public_src}/{tmp_folder}",
            item_name=last,
        )

    def __upload_one_file(
            self,
            sftp: SFTPClient,
            src_path: str,
            dest_path: str,
            file_name: str,
            file_size: [int] = 100
    ) -> bool:
        has_error = False
        try:
            with typer.progressbar(length=file_size, label=__("Copying %file_name%", {'file_name': file_name})) as progress:
                def __show_result_copy(size: int, full_size: int):
                    global old_value
                    progress.update(size - (old_value or 0))
                    old_value = size
                sftp.put(localpath=src_path, remotepath=f"{dest_path}", callback=__show_result_copy)
            typer.echo(__('Copy of %file_name% completed successfully', {'file_name': file_name}))
        except FileNotFoundError as err:
            app_logger.exception(f"Error uploading file {file_name} to container (file not found): {err}")
            typer.echo(__("Error uploading file: file not found on server"))
            has_error = True
        except Exception as err2:
            typer.echo(err2)
            app_logger.exception(f"Error uploading file {file_name} to container: {err2}")
            typer.echo(__("Error uploading file: undefined server error"))
            has_error = True

        return has_error

    def __upload_one_file_new(
            self,
            sftp: SFTPClient,
            src_path: str,
            dest_path: str,
            file_name: str,
            file_size: [int] = 100
    ) -> bool:
        has_error = False
        try:
            with typer.progressbar(length=file_size, label=__("Copying %file_name%", {'file_name': file_name})) as progress:
                def __show_result_copy(size: int, full_size: int):
                    global old_value
                    progress.update(size - (old_value or 0))
                    old_value = size
                sftp.put(localpath=src_path, remotepath=f"{dest_path}", callback=__show_result_copy)
            typer.echo(__('Copy of %file_name% completed successfully', {'file_name': file_name}))
        except FileNotFoundError as err:
            app_logger.exception(f"Error uploading file {file_name} to container (file not found): {err}")
            typer.echo(__("Error uploading file: file not found on server"))
            has_error = True
        except Exception as err2:
            typer.echo(err2)
            app_logger.exception(f"Error uploading file {file_name} to container: {err2}")
            typer.echo(__("Error uploading file: undefined server error"))
            has_error = True

        return has_error

    def __make_dirs_by_sftp(
            self,
            sftp: SFTPClient,
            path: str,
    ):
        full_path = ''
        for item in path.split('/'):
            if item == '':
                continue
            try:
                full_path += f'/{item}'
                sftp.chdir(full_path)  # Test if remote_path exists
            except IOError:
                sftp.mkdir(full_path)  # Create remote_path
                sftp.chdir(full_path)

    def __upload_list_files(
            self,
            sftp: SFTPClient,
            src_item: FileItemEntity,
            dest_path: str,
    ):
        if src_item.is_file:
            # need create folder if use dynamic folder
            paths = dest_path.split('/')
            new_name_file = paths[-1]
            real_dest_path = '/'.join(paths[0:-1])
            self.__make_dirs_by_sftp(sftp=sftp, path=real_dest_path)

            self.__upload_one_file(
                sftp=sftp,
                src_path=src_item.path,
                dest_path=dest_path,
                file_name=new_name_file,
                file_size=src_item.file_size,
            )
        elif src_item.is_folder:
            self.__make_dirs_by_sftp(sftp=sftp, path=dest_path)
            #server_dir = f"{dest_path}/{src_item.name}"
            #self.__make_dirs_by_sftp(sftp=sftp, path=server_dir)

            for item in src_item.children:
                self.__upload_list_files(
                    sftp=sftp,
                    src_item=item,
                    dest_path=f"{dest_path}/{item.name}",
                )

    def __upload_list_files_new(
            self,
            sftp: SFTPClient,
            src_item: SftpFileItemEntity,
    ):
        if src_item.is_file:

            get_parent_path = '/'.join(src_item.instance_path.split('/')[0:-1])
            self.__make_dirs_by_sftp(sftp=sftp, path=get_parent_path)

            self.__upload_one_file_new(
                sftp=sftp,
                src_path=src_item.path,
                dest_path=src_item.instance_path,
                file_name=src_item.name,
                file_size=src_item.file_size,
            )
        elif src_item.is_folder:
            self.__make_dirs_by_sftp(sftp=sftp, path=src_item.instance_path)
            for item in src_item.children:
                self.__upload_list_files_new(
                    sftp=sftp,
                    src_item=item,
                )

    def __download_one_file(
            self,
            sftp: SFTPClient,
            src_path: str,
            dest_path: str,
            file_name: str,
            file_size: [int] = 100
    ) -> bool:
        has_error = False
        try:
            with typer.progressbar(length=file_size, label=__("Copying %file_name%", {'file_name': file_name})) as progress:
                def __show_result_copy(size: int, full_size: int):
                    global old_value
                    progress.update(size - (old_value or 0))
                    old_value = size
                sftp.get(remotepath=src_path, localpath=f"{dest_path}", callback=__show_result_copy)
            typer.echo(__('Copy of %file_name% completed successfully%', {'file_name': file_name}))
        except FileNotFoundError as err:
            app_logger.exception(f"Error retrieving file {file_name} from container (file not found): {err}")
            typer.echo(__("Error retrieving file: file not found on server"))
            has_error = True
        except Exception as err2:
            typer.echo(err2)
            app_logger.exception(f"Error retrieving file {file_name} from container: {err2}")
            typer.echo(__("Error retrieving file: undefined server error"))
            has_error = True

        return has_error

    def __download_list_files(
            self,
            sftp: SFTPClient,
            src_item: FileItemEntity,
            dest_path: str,
    ):
        if src_item.is_file:
            self.__file_system_service.get_path('/'.join(dest_path.split('/')[0:-1]), auto_create=True)
            self.__download_one_file(
                sftp=sftp,
                src_path=src_item.path,
                dest_path=dest_path,
                file_name=src_item.name,
                file_size=src_item.file_size,
            )
        elif src_item.is_folder:
            server_dir = self.__file_system_service.get_path(str(Path(dest_path).joinpath(src_item.name)), auto_create=True)
            for item in src_item.children:
                self.__download_list_files(
                    sftp=sftp,
                    src_item=item,
                    dest_path=str(server_dir.joinpath(item.name)) if item.is_file else str(server_dir),
                )

    def __download_list_files_new(
            self,
            sftp: SFTPClient,
            src_item: SftpFileItemEntity,
    ):
        if src_item.is_file:
            self.__file_system_service.get_path('/'.join(src_item.dest_path.split('/')[0:-1]), auto_create=True)
            self.__download_one_file(
                sftp=sftp,
                src_path=src_item.path,
                dest_path=src_item.dest_path,
                file_name=src_item.name,
                file_size=src_item.file_size,
            )
        elif src_item.is_folder:
            self.__file_system_service.get_path(str(Path(src_item.dest_path)), auto_create=True)
            for item in src_item.children:
                self.__download_list_files_new(
                    sftp=sftp,
                    src_item=item,
                    #dest_path=src_item.dest_path,
                )

    @staticmethod
    def find_sftp_server_path(
            client: SSHClient,
    ) -> Optional[str]:
        stdin, stdout, stderr = client.exec_command(f'whereis sftp-server', get_pty=True)
        for line in stdout.readlines():
            pre_line = line.replace('sftp-server:', '')
            for command in pre_line.strip().split(' '):
                tmp = command.strip()
                if tmp:
                    if tmp.endswith('/sftp-server'):
                        return tmp
        return None

    def copy_data_on_container(
            self,
            client: SSHClient,
            docker_name: str,
            src_path: str,
            dest_path: str,
            is_recursive: bool = False,
    ):
        self.start_command_on_container(
            client=client,
            docker_name=docker_name,
            command=['cp ' + ('-R' if is_recursive else '') + f' {src_path}' + f' {dest_path}'],
        )
        # TODO: dont now how, need check for copy end!!!!
        sleep(3)

    @staticmethod
    def start_command_on_container(
            client: SSHClient,
            docker_name: str,
            command: List[str],
            is_bash: bool = False,
    ):
        if is_bash:
            stdin, stdout, stderr = client.exec_command(f'docker exec -it {docker_name} /bin/bash -c "{";".join(command)}"', get_pty=True)
        else:
            stdin, stdout, stderr = client.exec_command(f'docker exec -it {docker_name}  {command[0]}', get_pty=True)
        for line in stdout.readlines():
            pass

    def upload_data_to_container(
            self,
            ip_address: str,
            username: str,
            docker_name: str,
            src_path: str,
            dest_path: str,
            path_helper: SftpPathHelper,
            is_folder: bool = False,
    ):
        has_error = False
        client: Optional[SSHClient] = self.__get_client(ip_address=ip_address, username=username)
        sftp_server_path = self.find_sftp_server_path(client=client)

        if not sftp_server_path:
            typer.echo(__('No sftp server is installed on your instance'))
            raise typer.Exit(1)

        chan = client.get_transport().open_session()
        #chan.exec_command("sudo su -c /usr/lib/openssh/sftp-server")
        chan.exec_command(f"sudo su -c {sftp_server_path}")
        sftp = paramiko.SFTPClient(chan)

        try:
            files: List[FileItemEntity] = self.__file_system_service.get_path_items(src_path)
            for item in files:
                self.__upload_list_files(
                    sftp=sftp,
                    src_item=item,
                    dest_path=path_helper.tmp_instance_path_with_name(),
                )

            if path_helper.tmp_folder_path:
                # copy to dest_path
                self.start_command_on_container(
                    client=client,
                    docker_name=docker_name,
                    command='cp ' + ('-R' if is_folder else '') + f' {path_helper.tmp_container_path_with_name()}' + f' {dest_path}',
                )

        except FileNotFoundError as err:
            app_logger.error(f"Error uploading file to container {ip_address}, user {username} (file not found): {err}")
            typer.echo(__("Error uploading file: file not found on server"))
            has_error = True
        finally:
            if path_helper.tmp_folder_path:
                self.start_command_on_container(
                    client=client,
                    docker_name=docker_name,
                    command='rm -R ' + f'{path_helper.tmp_folder_path}',
                )
            sftp.close()

        client.close()
        if has_error:
            typer.Exit(1)

    def __build_sftp_client(
            self,
            ip_address: str,
            username: str,
    ) -> Tuple[SSHClient, SFTPClient]:
        client: Optional[SSHClient] = self.__get_client(ip_address=ip_address, username=username)
        sftp_server_path = self.find_sftp_server_path(client=client)

        if not sftp_server_path:
            typer.echo(__('SFTP server is not installed on the server instance'))
            raise typer.Exit(1)

        chan = client.get_transport().open_session()
        # chan.exec_command("sudo su -c /usr/lib/openssh/sftp-server")
        chan.exec_command(f"sudo su -c {sftp_server_path}")
        sftp = paramiko.SFTPClient(chan)

        return client, sftp

    @staticmethod
    def _check_if_file_name_in_path(path: str, file_template: Optional[str] = None) -> bool:
        # strange logic
        file_name = path.split('/')[-1] if path else None
        if file_name and '.' in file_name:
            if file_template and '.' in file_template:
                extension = file_template.split('.')[-1]
                if extension in file_name:
                    return True
            else:
                return True
        return False

    @staticmethod
    def _get_parent_from_path(path: str) -> str:
        pre_path = '/'.join(path.split('/')[0:-1])
        if not pre_path:
            return '/'
        else:
            return pre_path

    def __build_local_path_by_mapping(
            self,
            files: List[FileItemEntity],
            instance_path: str,
            container_path: str,
            destination_path: str,
            with_tmp: bool = False,
            has_parent: bool = False,
    ):
        result = []
        for item in files:
            elem = SftpFileItemEntity.model_validate(item.model_dump())
            if item.is_file:
                has_file_name = self._check_if_file_name_in_path(
                    path=instance_path,
                    file_template=item.name,
                )

                if not has_parent and not with_tmp and has_file_name:
                    elem.instance_path = instance_path
                    elem.container_path = container_path
                else:
                    elem.instance_path = f"{instance_path}/{item.name}"
                    elem.container_path = f"{container_path}/{item.name}"

                if with_tmp:
                    has_file_name = self._check_if_file_name_in_path(
                        path=destination_path,
                        file_template=item.name,
                    )
                    if has_file_name:
                        elem.dest_path = destination_path
                    else:
                        elem.dest_path = f"{destination_path}/{item.name}"
                else:
                    elem.dest_path = elem.instance_path

            else:
                if not has_parent and not with_tmp:
                    elem.instance_path = instance_path
                    elem.container_path = container_path
                else:
                    elem.instance_path = f"{instance_path}/{item.name}"
                    elem.container_path = f"{container_path}/{item.name}"

                if with_tmp:
                    elem.dest_path = destination_path
                else:
                    elem.dest_path = elem.instance_path

            if len(item.children) > 0:
                elem.children = []
                elem.children.extend(self.__build_local_path_by_mapping(
                    files=item.children,
                    instance_path=elem.instance_path,
                    container_path=elem.container_path,
                    destination_path=elem.dest_path,
                    with_tmp=with_tmp,
                    has_parent=True,
                ))

            result.append(elem)

        return result

    def upload_data_to_container_new(
            self,
            ip_address: str,
            username: str,
            docker_name: str,
            src_path: str,
            dest_path: str,
            instance_path: str,
            container_path: str,
            is_folder: bool = False,
            tmp_path: Optional[str] = None,
    ):
        has_error = False
        client, sftp = self.__build_sftp_client(username=username, ip_address=ip_address)

        origin_files: List[FileItemEntity] = self.__file_system_service.get_path_items(src_path)

        files: List[SftpFileItemEntity] = self.__build_local_path_by_mapping(
            files=origin_files,
            instance_path=instance_path,
            container_path=container_path,
            destination_path=dest_path,
            with_tmp=True if tmp_path else False,
        )

        try:

            for item in files:
                self.__upload_list_files_new(
                    sftp=sftp,
                    src_item=item,
                )

            if tmp_path:
                # copy to dest_path
                self.start_command_on_container(
                    client=client,
                    docker_name=docker_name,
                    is_bash=True,
                    command=[
                        f"mkdir -p {self._get_parent_from_path(path=files[0].dest_path)}",
                        f"cp " + ("-R" if is_folder else "") + f" {files[0].container_path} " + f" {files[0].dest_path}",
                    ],
                )

        except FileNotFoundError as err:
            app_logger.error(f"Error uploading file to container {ip_address}, user {username} (file not found): {err}")
            typer.echo(__("Error uploading file: file not found on server"))
            has_error = True
        finally:
            if tmp_path:
                self.start_command_on_container(
                    client=client,
                    docker_name=docker_name,
                    command=['rm -R ' + f'{tmp_path}',],
                )
            sftp.close()

        client.close()
        if has_error:
            typer.Exit(1)

    def __read_remote_path_items(self, sftp: SFTPClient, folder: str) -> List[FileItemEntity]:
        path_items = []
        root_stat = sftp.stat(folder)
        parent = FileItemEntity(
            name=folder.split('/')[-1],
            path=folder,
            is_file=stat.S_ISREG(root_stat.st_mode),
            is_folder=stat.S_ISDIR(root_stat.st_mode),
            file_size=root_stat.st_size,
        )
        path_items.append(parent)
        if parent.is_folder:
            sftp.chdir(folder)
            for item in sftp.listdir_attr():
                next_path = f'{folder}/{item.filename}'
                is_dir = stat.S_ISDIR(item.st_mode)
                is_file = stat.S_ISREG(item.st_mode)
                if is_file:
                    parent.children.append(FileItemEntity(
                        name=item.filename,
                        path=next_path,
                        is_file=is_file,
                        is_folder=is_dir,
                        file_size=item.st_size,
                    ))
                elif is_dir:
                    parent.children.extend(self.__read_remote_path_items(
                        sftp=sftp,
                        folder=next_path,
                    ))
        return path_items

    def __read_remote_path_items_new(
            self,
            sftp: SFTPClient,
            folder: str,
            dest_path: str,
            instance_path: str,
            container_path: str,
            tmp_path: Optional[str] = False,
    ) -> List[SftpFileItemEntity]:
        path_items = []
        try:
            root_stat = sftp.stat(folder)
            parent = SftpFileItemEntity(
                name=folder.split('/')[-1],
                path=folder,
                is_file=stat.S_ISREG(root_stat.st_mode),
                is_folder=stat.S_ISDIR(root_stat.st_mode),
                file_size=root_stat.st_size,
                instance_path=instance_path,
                container_path=container_path,
                dest_path=dest_path,
            )
            path_items.append(parent)
            if parent.is_file:
                has_file_name = self._check_if_file_name_in_path(
                    path=instance_path,
                    file_template=dest_path,
                )
                if not has_file_name:
                    parent.dest_path += f"{parent.name}" if parent.dest_path.endswith('/') else f"/{parent.name}"

            elif parent.is_folder:
                sftp.chdir(folder)
                parent.dest_path += f"{parent.name}" if parent.dest_path.endswith('/') else f"/{parent.name}"
                for item in sftp.listdir_attr():
                    next_path = f'{folder}/{item.filename}'
                    is_dir = stat.S_ISDIR(item.st_mode)
                    is_file = stat.S_ISREG(item.st_mode)
                    if is_file:
                        parent.children.append(SftpFileItemEntity(
                            name=item.filename,
                            path=next_path,
                            is_file=is_file,
                            is_folder=is_dir,
                            file_size=item.st_size,
                            instance_path=f'{instance_path}/{item.filename}',
                            container_path=f'{container_path}/{item.filename}',
                            dest_path=f'{parent.dest_path}/{item.filename}',
                        ))
                    elif is_dir:
                        parent.children.extend(self.__read_remote_path_items_new(
                            sftp=sftp,
                            folder=next_path,
                            dest_path=parent.dest_path,
                            instance_path=parent.instance_path,
                            container_path=parent.container_path,
                            tmp_path=tmp_path,
                        ))
            return path_items
        except FileNotFoundError as ex:
            app_logger.exception(f"Unable to read remote file list: {ex}")
            typer.echo(__('Source path not found: check the command parameters'))
            typer.Exit(1)
        except Exception as ex:
            app_logger.exception(f"Error occurred: {ex}")
            typer.echo(__('Error occurred while processing the file'))
            typer.Exit(1)

    def download_data_to_container(
            self,
            ip_address: str,
            username: str,
            docker_name: str,
            src_path: str,
            dest_path: str,
            path_helper: SftpPathHelper,
            is_folder: bool = False,
    ):
        has_error = False
        client: Optional[SSHClient] = self.__get_client(ip_address=ip_address, username=username)

        sftp_server_path = self.find_sftp_server_path(client=client)

        if not sftp_server_path:
            typer.echo(__('SFTP server is not installed on the server instance'))
            raise typer.Exit(1)

        chan = client.get_transport().open_session()
        #chan.exec_command("sudo su -c /usr/lib/openssh/sftp-server")
        chan.exec_command(f"sudo su -c {sftp_server_path}")
        sftp = paramiko.SFTPClient(chan)

        try:
            if path_helper.tmp_folder_path:
                self.__make_dirs_by_sftp(sftp=sftp, path=path_helper.tmp_instance_path)
                self.copy_data_on_container(
                    client=client,
                    docker_name=docker_name,
                    is_recursive=is_folder,
                    src_path=src_path,
                    dest_path=path_helper.tmp_container_path if is_folder else path_helper.tmp_container_path_with_name(),
                )

            files: List[FileItemEntity] = self.__read_remote_path_items(
                sftp=sftp,
                folder=path_helper.tmp_instance_path_with_name(),
            )

            for item in files:
                self.__download_list_files(
                    sftp=sftp,
                    src_item=item,
                    dest_path=dest_path,
                )
        except FileNotFoundError as err:
            print(err)
            app_logger.error(f"Error uploading file to container {ip_address} for user {username} (file not found): {err}")
            typer.echo(__("Error uploading file: file not found on server"))
            has_error = True
        finally:
            if path_helper.tmp_folder_path:
                # remove temporary path
                self.start_command_on_container(
                    client=client,
                    docker_name=docker_name,
                    command='rm -R ' + f'{path_helper.tmp_folder_path}',
                )
            sftp.close()

        client.close()
        if has_error:
            typer.Exit(1)

    def __copy_data_from_inner_path_to_mapping(
            self,
            client: SSHClient,
            sftp: SFTPClient,
            docker_name: str,
            src_path: str,
            instance_path: str,
            tmp_path: Optional[str] = False,
            is_folder: bool = False,
    ) -> str:
        # added copy file to public
        pre_copy_path = tmp_path
        pre_path = instance_path
        if tmp_path:
            src_path_name = src_path.split('/')[-1]
            if not pre_copy_path.endswith('/'):
                pre_copy_path += '/'
            pre_copy_path += src_path_name
            if not pre_path.endswith('/'):
                pre_path += '/'
            pre_path += src_path_name

            self.__make_dirs_by_sftp(sftp=sftp, path=instance_path)
            self.copy_data_on_container(
                client=client,
                docker_name=docker_name,
                is_recursive=is_folder,
                src_path=src_path,
                dest_path=pre_copy_path,
            )
        return pre_path

    def download_data_from_container_new(
            self,
            ip_address: str,
            username: str,
            docker_name: str,
            src_path: str,
            dest_path: str,
            instance_path: str,
            container_path: str,
            tmp_path: Optional[str] = False,
            is_folder: bool = False,
    ):
        has_error = False

        client, sftp = self.__build_sftp_client(username=username, ip_address=ip_address)

        try:
            # added copy file to public
            pre_path = self.__copy_data_from_inner_path_to_mapping(
                client=client,
                sftp=sftp,
                docker_name=docker_name,
                src_path=src_path,
                instance_path=instance_path,
                tmp_path=tmp_path,
                is_folder=is_folder,
            )

            files: List[SftpFileItemEntity] = self.__read_remote_path_items_new(
                sftp=sftp,
                folder=pre_path,
                instance_path=instance_path,
                container_path=container_path,
                tmp_path=tmp_path,
                dest_path=dest_path,
            )

            if not is_folder and files[0].is_folder:
                typer.echo(__("The specified path is a directory: enable the recursive flag"))
                raise typer.Exit(1)

            for item in files:
                self.__download_list_files_new(
                    sftp=sftp,
                    src_item=item,
                    #dest_path=result_path,
                )
        except FileNotFoundError as err:
            print(err)
            app_logger.error(f"Error uploading file to container {ip_address} for user {username} (file not found): {err}")
            typer.echo(__("Error uploading file: file not found on server"))
            has_error = True
        finally:
            if tmp_path:
                # remove temporary path
                self.start_command_on_container(
                    client=client,
                    docker_name=docker_name,
                    command=['rm -R ' + f'{tmp_path}'],
                )
            sftp.close()

        client.close()
        if has_error:
            typer.Exit(1)

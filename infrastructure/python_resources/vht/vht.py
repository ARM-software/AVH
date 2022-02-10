import logging
import sys
from vht import aws

class VHTClient():
    def __init__(self, backend):
        self.backend_desc = backend.lower()
        logging.info(f"vht:{self.backend_desc} backend selected!")
        self._set_backend()

    def _set_backend(self):
        if self.backend_desc == "aws":
            self.backend = aws.AWSClient()
        else:
            logging.error(f"{self.backend_desc} not supported!")
            sys.exit(-1)

    def create_instance(self):
        return self.backend.create_instance()

    def delete_file_from_cloud(self, key):
        return self.backend.delete_file_from_cloud(key)

    def download_file_from_cloud(self, filename, key):
        return self.backend.download_file_from_cloud(filename, key)

    def get_image_id(self):
        return self.backend.get_image_id()

    def get_instance_state(self):
        return self.backend.get_instance_state()

    def get_process_vht_commands(self):
        return self.backend.get_process_vht_commands()

    def run(self):
        return self.backend.run()

    def send_remote_command(self, command_list, working_dir, fail_if_unsuccess = True):
        return self.backend.send_remote_command(command_list=command_list,
                                                working_dir=working_dir,
                                                fail_if_unsuccess=fail_if_unsuccess)

    def send_remote_command_batch(self, command_list, working_dir, fail_if_unsuccess = True):
        return self.backend.send_remote_command_batch(
                                                command_list=command_list,
                                                working_dir=working_dir,
                                                fail_if_unsuccess=fail_if_unsuccess)

    def start_instance(self):
        return self.backend.start_instance()

    def stop_instance(self):
        return self.backend.stop_instance()

    def terminate_instance(self):
        return self.backend.terminate_instance()

    def teardown(self):
        return self.backend.teardown()

    def upload_file_to_cloud(self, filename, key):
        return self.backend.upload_file_to_cloud(filename, key)

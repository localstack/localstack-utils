class LocalstackDockerConfiguration:
    pull_new_image = False
    randomize_ports = False
    image_name = None
    image_tag = None
    platform = None

    gateway_listen = "0.0.0.0:4566"
    environment_variables = {}
    port_mappings = {}
    bind_mounts = {}

    initialization_token = None
    use_dingle_docker_container = False
    ignore_docker_runerrors = False
    pro = False
    auto_remove_container = False

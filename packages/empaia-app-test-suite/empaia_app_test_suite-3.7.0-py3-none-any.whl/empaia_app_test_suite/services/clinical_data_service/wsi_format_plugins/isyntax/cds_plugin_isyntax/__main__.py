from cds_plugin_utils.backend_server import BackendServer

if __name__ == "__main__":
    server = BackendServer(plugin_module="cds_plugin_isyntax", plugin_class_name="IsyntaxSlideInstance")
    server.run()

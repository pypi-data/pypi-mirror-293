from ...exceptions import ConfigValidationError, EadContentValidationError
from ..common import _validate_class_value, _validate_reference_type, get_valid_class_values


def validate_ead(ead, namespaces):
    io_mode_refs = set()
    if "rendering" in ead:
        _validate_rendering(ead, namespaces)
    for mode_name, mode_spec in ead["modes"].items():
        _validate_mode(ead, mode_name, mode_spec, io_mode_refs)
        for io_key, io_spec in ead["io"].items():
            _validate_io_item_recursive(ead, mode_spec, io_key, io_spec, namespaces)
    for io_key in ead["io"]:
        if io_key not in io_mode_refs:
            raise EadContentValidationError(f"Unreferenced item in io section: io.{io_key} is not used by any mode")


def validate_global_config(ead, config):
    config_spec = ead.get("configuration", {}).get("global", {})
    _validate_config_section(config, config_spec)


def validate_customer_config(ead, config):
    config_spec = ead.get("configuration", {}).get("customer", {})
    _validate_config_section(config, config_spec)


def _validate_config_section(config, config_spec):
    config = config if config else {}
    for key, entry_spec in config_spec.items():
        if not entry_spec.get("optional", False) and key not in config:
            raise ConfigValidationError(f"Parameter {key} is missing in given configuration")
        if key in config:
            # str[ing], int[eger], bool, float
            if not entry_spec["type"].startswith(type(config[key]).__name__):
                raise ConfigValidationError(f"Parameter {key} has wrong type in given configuration")
    for key in config.keys():
        if key not in config_spec:
            raise ConfigValidationError(f"Parameter {key} is not part of the configuration specification")


def _validate_mode(ead, mode_name, mode_spec, io_mode_refs):
    for i_or_o in ("inputs", "outputs"):
        for io_key in mode_spec[i_or_o]:
            if io_key not in ead["io"]:
                raise EadContentValidationError(
                    f"Unresolved {i_or_o} for mode {mode_name}: {io_key} not found in io section"
                )
            other_i_or_o = "inputs" if i_or_o == "outputs" else "outputs"
            if io_key in mode_spec[other_i_or_o]:
                raise EadContentValidationError(f"Mode {mode_name} defines non-disjoint inputs and outputs: {io_key}")
            io_mode_refs.add(io_key)
    if mode_name == "standalone" or mode_name == "preprocessing":
        if not mode_spec.get("containerized", True):
            raise EadContentValidationError(f"{mode_name} mode must not be uncontainerized")
    elif mode_name == "postprocessing":
        if "containerized" not in mode_spec:
            raise EadContentValidationError("postprocessing mode must specify containerized flag")
    else:  # report
        if mode_spec.get("containerized", False):
            raise EadContentValidationError("report mode must not be containerized")
    if mode_name == "preprocessing":
        if len(mode_spec["inputs"]) != 1 or ead["io"][mode_spec["inputs"][0]]["type"] != "wsi":
            raise EadContentValidationError("Mode preprocessing requires exactly one input of type wsi")


def _validate_io_item_recursive(ead, mode_spec, io_key, io_spec, namespaces):
    if "reference" in io_spec:
        _validate_reference(ead, mode_spec, io_key, io_spec)
    if "classes" in io_spec:
        _validate_classes(ead, mode_spec, io_key, io_spec, namespaces)
    if "channel_classes" in io_spec or "element_mapping" in io_spec:
        _validate_class_mapping(ead, io_key, io_spec, namespaces)
    if io_spec["type"] == "collection":
        _validate_io_item_recursive(ead, mode_spec, io_key + ".items", io_spec["items"], namespaces)


def _validate_reference(ead, mode_spec, io_key, io_spec):
    _, ref_key, *ref_tail = io_spec["reference"].split(".")
    if io_key in mode_spec["inputs"] and ref_key in mode_spec["outputs"]:
        raise EadContentValidationError(f"Inputs must not reference outputs (io.{io_key} -> {io_spec['reference']})")
    reference = ead["io"]
    for node in [ref_key] + ref_tail:
        if node not in reference:
            raise EadContentValidationError(f"{io_spec['reference']} referenced by io.{io_key} not found")
        reference = reference[node]
    _validate_reference_type(io_spec["type"], reference["type"])


def _validate_classes(ead, mode_spec, io_key, io_spec, namespaces):
    if io_key in mode_spec["outputs"]:
        raise EadContentValidationError("Outputs must not have class constraints")
    for class_value in io_spec["classes"]:
        _validate_class_value(ead, class_value, namespaces)


def _validate_class_mapping(ead, io_key, io_spec, namespaces):
    valid_class_values = get_valid_class_values(ead, namespaces, with_root=True)
    for mapping_class in io_spec.get("channel_classes", {}):
        if mapping_class not in valid_class_values:
            raise EadContentValidationError(
                f"channel_classes for {io_key} contains invalid class value {mapping_class}"
            )
    for mapping_class in io_spec.get("element_classes", {}):
        if mapping_class not in valid_class_values:
            raise EadContentValidationError(
                f"element_classes for {io_key} contains invalid class value {mapping_class}"
            )


def _validate_rendering(ead, namespaces):
    valid_class_values = get_valid_class_values(ead, namespaces)
    rendering_spec = ead.get("rendering", {})
    _validate_rendering_section(rendering_spec, valid_class_values)


def _validate_rendering_section(rendering_specs, valid_classes):
    for spec_type, rendering_spec in rendering_specs.items():
        for spec in rendering_spec:
            if spec["class_value"] not in valid_classes:
                raise EadContentValidationError(
                    f"Rendering for {spec_type} contains invalid class value {spec['class_value']}"
                )

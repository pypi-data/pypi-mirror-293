from ..exceptions import EadContentValidationError

ANNOTATION_TYPES = ("point", "line", "arrow", "rectangle", "polygon", "circle")
PRIMITIVE_TYPES = ("bool", "integer", "float", "string")
PIXELMAP_TYPE = ("continuous_pixelmap", "discrete_pixelmap", "nominal_pixelmap")


def _validate_class_value(ead, class_value, namespaces):
    split_target = ".classes."
    if class_value.endswith(".classes"):
        split_target = ".classes"
    if split_target not in class_value:
        raise EadContentValidationError(f"Class value {class_value} is malformed")
    class_namespace, class_suffix = class_value.split(split_target)
    if class_namespace.startswith("org.empaia.global."):
        for namespace_id, namespace in namespaces.items():
            if namespace_id == class_namespace:
                class_node = namespace["classes"]
                break
        else:
            raise EadContentValidationError(f"Global namespace not found for class value {class_value}")
    elif class_namespace == f"{ead['namespace']}":
        class_node = ead.get("classes", {})
    else:
        raise EadContentValidationError(f"Namespace not valid for class value {class_value}")

    if class_suffix:  # empty if class value is the classes root
        for item in class_suffix.split("."):
            if item not in class_node:
                raise EadContentValidationError(f"Class value {class_value} not found in class hierarchy")
            class_node = class_node[item]


def _validate_reference_type(source_type, target_type):
    if source_type == "collection":
        if target_type != "wsi" and target_type not in ANNOTATION_TYPES:
            raise EadContentValidationError("Collections may only reference WSIs or annotations")
    if source_type in PRIMITIVE_TYPES:
        if target_type != "wsi" and target_type != "collection" and target_type not in ANNOTATION_TYPES:
            raise EadContentValidationError("Primitives may only reference WSIs, collections or annotations")
    if source_type in ANNOTATION_TYPES:
        if target_type != "wsi":
            raise EadContentValidationError("Annotations must reference WSIs")
    if source_type in PIXELMAP_TYPE:
        if target_type != "wsi":
            raise EadContentValidationError("Pixelmaps must reference WSIs")
    if source_type == "class":
        if target_type not in ANNOTATION_TYPES:
            raise EadContentValidationError("Classes must reference annotations")


def get_valid_class_values(ead, namespaces, with_root=False):
    global_classes = _get_global_class_values(namespaces, with_root=with_root)
    ead_classes = _get_ead_class_values(ead, with_root=with_root)
    classes = global_classes + ead_classes
    return classes


def _get_global_class_values(namespaces, with_root=False):
    global_classes = []
    for namespace_id, namespace in namespaces.items():
        root = f"{namespace_id}.classes"
        if with_root:
            global_classes.append(root)
        for class_name in namespace["classes"]:
            class_value = f"{root}.{class_name}"
            global_classes.append(class_value)
    return global_classes


def _get_ead_class_values(ead, with_root=False):
    if "classes" not in ead:
        return []
    ead_classes = []
    namespace = ead["namespace"]
    root = f"{namespace}.classes"
    if with_root:
        ead_classes.append(root)
    for value in _get_class_values_recursive(ead["classes"], with_root=with_root):
        ead_classes.append(f"{root}.{value}")
    return ead_classes


def _get_class_values_recursive(classes, with_root=False, prefix=None):
    class_values = []
    for class_name, cl in classes.items():
        if "name" in cl:
            if prefix:
                class_values.append(f"{prefix}.{class_name}")
            else:
                class_values.append(class_name)
        else:
            if with_root:
                class_values.append(class_name)
            values = _get_class_values_recursive(cl, with_root=with_root, prefix=class_name)
            class_values.extend(values)
    return class_values

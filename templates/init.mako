# Class: ${module_name}
# ===========================
#
class ${module_name} (
  $install_version = $${module_name}::params::install_version
) inherits ${module_name}::params {
  class {"::${module_name}::v${install_version}":  }
}

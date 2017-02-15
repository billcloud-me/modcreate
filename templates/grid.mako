class ${module_name}::v1_0_0 {
  % for package_name, package_version in packages.items():
  package { '${package_name}: ensure => '${package_version}' }
  % endfor
}

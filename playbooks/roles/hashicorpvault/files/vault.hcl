# files/vault.hcl
storage "file" {
  path = "/etc/vault.d/data"
}

listener "tcp" {
  address     = "192.168.1.150:8200"
  tls_disable = 1
}

ui = true

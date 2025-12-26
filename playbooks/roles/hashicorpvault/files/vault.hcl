# files/vault.hcl
storage "file" {
  path = "/etc/vault.d/data"
}

listener "tcp" {
  address     = "127.0.0.1:8200"
  tls_disable = 1
}

ui = true

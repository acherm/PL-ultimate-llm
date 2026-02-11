require 'bud'

class KVS
  include Bud

  state do
    table :kvs, [:key] => [:value]
    channel :put_req, [:@addr, :key, :value]
    channel :get_req, [:@addr, :key]
    channel :get_resp, [:@addr, :key, :value]
  end

  bloom do
    kvs <+ put_req {|r| [r.key, r.value]}
    get_resp <~ (get_req * kvs).pairs(:key => :key) {|r, kv| [r.addr, kv.key, kv.value]}
  end
end

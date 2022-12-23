# webstress
Python script that uses aiohttp to chuck tons of requests at one or more URLs and measures throughput
Originally built to see how much throughput I can get on a Rasperry Pi model 4b, running Elixir Phoenix web framework
and serving over a VPS-proxied node over [Yggdrasil Network](https://yggdrasil-network.github.io/)

Uses `aiohttp` to stack up requests. See parameter `--help` for options. 

### TODO
* rate calculation is printed a bit too frequently and should probably be accumulated over time. 

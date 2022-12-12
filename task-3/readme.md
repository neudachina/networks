## отчет
была построена необходимая топология, указанная в задании 

<img src="https://github.com/neudachina/networks/blob/main/task-3/pics/topology.jpg" alt="topology" width="1000"/>

доказательство корректности ip-адресов, пинга внешнего роутера (ip-адрес у него настроен
как `10.0.0.2`) и пинга друг друга на обоих клиентах 

<img src="https://github.com/neudachina/networks/blob/main/task-3/pics/client-1.jpg" alt="ping client-1" width="500"/> <img src="https://github.com/neudachina/networks/blob/main/task-3/pics/client-2.jpg" alt="ping client-2" width="500"/>

заметим, что обоих клиентам выдались ip-адреса вида 10.0.X.11, 
потому что первые десять ip-адресов были заблокированы во время конфигурации.
доказательство корректности работы NAT и DHCP

<img src="https://github.com/neudachina/networks/blob/main/task-3/pics/nat.jpg" alt="nat" width="500"/> <img src="https://github.com/neudachina/networks/blob/main/task-3/pics/dhcp.jpg" alt="dhcp" width="500"/> 


доказательство отсутсвия дополнительных маршрутов в сети клиентов на верхнем маршрутизаторе

<img src="https://github.com/neudachina/networks/blob/main/task-3/pics/routing.jpg" alt="routing" width="750"/> 


итого: я добилась выполнения всех пунктов и подпунктов 


## используемые инструкции

### clients
```
ip dhcp
```

### switch-1
```
enable
configure terminal
vtp mode transparent
vlan 10
vlan 20
exit

interface e0/1 
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q 
switchport mode trunk

interface e0/3
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q
switchport mode trunk

interface e0/0
switch mode access
switch access vlan 10
exit
exit
exit

```

### switch-2
```
enable
configure terminal
vtp mode transparent
vlan 10
vlan 20
exit

interface e0/2
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q 
switchport mode trunk

interface e0/3
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q
switchport mode trunk

interface e0/0
switch mode access
switch access vlan 20
exit
exit
exit

```


### switch-0
```
enable
configure terminal
vtp mode transparent
vlan 10
vlan 20
exit

spanning-tree vlan 10 root primary
spanning-tree vlan 20 root primary

interface e0/0
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q 
switchport mode trunk

interface e0/1
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q 
switchport mode trunk

interface e0/2
switchport trunk allowed vlan 10
switchport trunk allowed vlan 20
switchport trunk encapsulation dot1q 
switchport mode trunk

exit
exit
exit
```

### router-1
```
enable
configure terminal
interface e0/0
no shutdown
exit

interface e0/0.10
encapsulation dot1Q 10
ip address 10.0.10.1 255.255.255.0

interface e0/0.20
encapsulation dot1Q 20
ip address 10.0.20.1 255.255.255.0
exit

ip dhcp excluded-address 10.0.10.1 10.0.10.10
ip dhcp excluded-address 10.0.20.1 10.0.20.10

ip dhcp pool 10
network 10.0.10.0 255.255.255.0
default-router 10.0.10.1
dns-server 100.100.100.100


ip dhcp pool 20
network 10.0.20.0 255.255.255.0
default-router 10.0.20.1
dns-server 100.100.100.100
exit

interface e0/0
ip nat inside
exit

interface e0/0.10
ip nat inside

interface e0/0.20
ip nat inside
exit

interface e0/1
ip address 10.0.0.1 255.255.255.0
no shutdown
ip nat outside
exit

ip nat pool POOL 10.0.0.1 10.0.0.255 netmask 255.255.255.0
access-list 100 permit ip 10.0.10.0 0.0.0.255 any
access-list 100 permit ip 10.0.20.0 0.0.0.255 any
ip nat inside source list 100 pool POOL

exit
exit
```

### router-2
```
enable
configure terminal 
interface e0/1
ip address 10.0.0.2 255.255.255.0
no shutdown
exit
exit
exit
```

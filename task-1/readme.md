## отчет
была построена необходимая топология, указанная в задании 

<img src="/pics/topology.jpg" alt="topology" width="500"/>

все startup-конфиги можно посмотреть в соответствующей папке confings. 
сеть будет работать даже при потере одно из соединений между switch'ами за счет того, что spanning-tree 
самостоятельно перестроится. STP, кстати, включён по умолчанию на всех коммутаторах cisco, так что ничего дополнительно
для этого я не прописывала. линк между коммутаторами уровня доступа заблокирован, так как switch-0 является
корнем для обоих подсетей, так что, если не произошло никаких падений, через него будут проходить все пакеты

доказательство корректности пингов на обоих клиентах 

<img src="/pics/ping client-1.jpg" alt="ping client-1" width="500"/> <img src="/pics/ping client-2.jpg" alt="ping client-2" width="500"/>

доказательство корректности spanning-tree на разных коммутаторах 
(слева направо и сверху вниз switch-{0, 1, 2} в порядке возрастания)

<img src="/pics/spanning-tree switch-0.jpg" alt="switch-0" width="500"/> <img src="/pics/spanning-tree switch-1.jpg" alt="switch-1" width="500"/> <img src="/pics/spanning-tree switch-2.jpg" alt="switch-2" width="500"/> 


итого: я добилась выполнения всех пунктов и подпунктов 


## используемые инструкции

### client-1
```
ip 10.0.10.2 255.255.255.0 10.0.10.1
```

### client-2
```
ip 10.0.20.2 255.255.255.0 10.0.20.1
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

### router
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
exit
exit
```

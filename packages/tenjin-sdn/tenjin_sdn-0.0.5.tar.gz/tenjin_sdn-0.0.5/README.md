# Tenjin SDN (For Python)

This Project is want to implement [Tenjin SDN](https://github.com/Arikato111/Tenjin) for python. Tenjin is The sdn framework that you can use for control network.

## Installation

### install tenjin with pip

```bash
pip install tenjin_sdn
```

### Install from source

```bash
git clone https://github.com/Arikato111/Tenjin-py
cd Tenjin-py
pip install .
```

## Example

### With openflow 1.3

```python
from tenjin_sdn import Ctrl13

controller = Ctrl13(address="127.0.0.1", port=6653)
controller.run()
```

### With openflow 1.0

```python
from tenjin_sdn import Ctrl10

controller = Ctrl10(address="0.0.0.0", port=6653)
controller.run()
```

## Mininet

Mininet is a network emulator to create virtual networks for rapid prototyping of Software-Defined.
Using mininet for testing this SDN Framework.

### Run Mininet with Openflow 1.3

```bash
sudo mn --controller=remote,ip=127.0.0.1 --mac --switch=ovsk,protocols=OpenFlow13 --topo=tree,2
```

### Run Mininet with Openflow 1.0

```bash
sudo mn --controller=remote,ip=127.0.0.1 --mac --switch=ovsk,protocols=OpenFlow10 --topo=tree,2
```

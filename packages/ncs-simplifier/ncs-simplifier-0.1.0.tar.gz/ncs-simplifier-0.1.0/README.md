# NCS Simplifier

NCS Simplifier é uma biblioteca Python que simplifica a interação com dispositivos de rede utilizando Cisco NSO. 

## Instalação

Para instalar a biblioteca, execute:

pip install ncs-simplifier

## Uso

Veja um exemplo de como usar a biblioteca:

```python
import ncs
from ncs_simplifier import get_vendor_name

def main():
    with ncs.maapi.single_read_trans('admin', 'python', groups=['admin']) as trans:
        root = ncs.maagic.get_root(trans)
        device = root.devices.device['nome_do_dispositivo']  # Substituir pelo nome do dispositivo
        
        # Identifica o vendor do dispositivo
        vendor_name = get_vendor_name(device)
        print(f"Vendor identificado: {vendor_name}")

if __name__ == '__main__':
    main()

```
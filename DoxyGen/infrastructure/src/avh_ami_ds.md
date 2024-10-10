# Debug with Arm Development Studio {#debug_ds}

This section explains how [Arm Development Studio](https://developer.arm.com/tools-and-software/embedded/arm-development-studio) can be used for debugging your embedded application that runs on AVH AMI.

## Tools Installation and set up {#ds_setup}

[Download](https://developer.arm.com/tools-and-software/embedded/arm-development-studio/downloads) and install the latest Arm Development Studio. If necessary, you can generate an evaluation license from _Help > Arm License Manager_.

Use SSH port forwarding to forward the port to be used for debug server (default is `7100`) on your virtual target to your localhost.
```
ssh -i <key.pem> -N -L 7100:localhost:7100 ubuntu@<AMI_IP_addr>
```

The `-N` option holds the SSH tunnel connection and does not allow to execute other remote commands. This is useful when only forwarding ports.

## Start program on the remote FVP model {#ds_vht_start}

- Add following [command line options](../../simulation/html/using.html#Options) when launching a program on the FVP target in the AMI:
|**Option**             |**Alias**|
| ----------------------| ------- |
| `--iris-server`       | `-I`    |
| `--iris-allow-remote` | `-A`    |
| `--iris-port <PORT>`  |         |
| `--print-port-number` | `-p`    |

Use `--help` for a full description of these options.

**Example**

```
VHT_Corstone_SSE-300_Ethos-U55 <other launching options> -I -A --iris-port 7100 -p
```

This will start the debug server with remote connection enabled on port `7100`.

## Connect to Target in Arm DS {#ds_connect}

- From the menu, select _File > New > Model Connection_, and give the connection a meaningful name
- Search for `VHT` to show all supported models, and select appropriate target
- In the _Connections_ tab, specify to connect to an already running model at `localhost:<port>`<br>
![Connections Tab](images/debug_config1.png)

- In the _Files_ tab, specify the local ELF image to load debug symbols from<br>
![Files Tab](images/debug_config2b.png)

- Click _Debug_ to connect to the virtual target, and commence your debug session

For more information see the Arm Development Studio [documentation](https://developer.arm.com/documentation/101469/latest/Debugging-code/Configuring-a-connection-to-an-external-Fixed-Virtual-Platform--FVP--for-bare-metal-application-debug).

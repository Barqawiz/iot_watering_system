// Base application https://github.com/rickyhh2/flutter_rpi_bluetooth_client
// some portions of code developed by ChatGPT and modified accordingly
// all other files were only modified for compilation purposes and versioning concerns

import 'package:flutter/material.dart';
import 'AppPage.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:permission_handler/permission_handler.dart';

import 'ChatPage.dart';
//import './ChatPage2.dart';


class MainPage extends StatefulWidget {
  @override
  _MainPage createState() => new _MainPage();
}

class _MainPage extends State<MainPage> {


  bool connected = false;
  BluetoothDevice _device = BluetoothDevice(name: 'MyDevice', address: '00:00:00:00', type: BluetoothDeviceType.classic);

  @override
  void initState() {
    super.initState();
    requestPermissions();
    _initializeBluetooth();
  }

  Future<void> requestPermissions() async {
    Map<Permission, PermissionStatus> statuses = await [
      Permission.bluetoothScan,
      Permission.bluetoothConnect,
      Permission.location,
    ].request();

    if (statuses[Permission.bluetoothScan]!.isGranted &&
        statuses[Permission.bluetoothConnect]!.isGranted &&
        statuses[Permission.location]!.isGranted) {
      print('All permissions granted');
    } else {
      print('Some permissions are still not granted');
    }
  }

  void _initializeBluetooth() async {
    try {
      List<BluetoothDevice> bondedDevices = await FlutterBluetoothSerial.instance.getBondedDevices();
      FlutterBluetoothSerial.instance
        .getBondedDevices()
        .then((List<BluetoothDevice> bondedDevices) {
      setState(() {
          for(BluetoothDevice device in bondedDevices){
            print(device.name);
            if (device.name == "raspberrypi"){
              _device = device;
            }
          }
        });
      });
      print('Bonded Devices: $bondedDevices');
    } catch (e) {
      print('Error while getting bonded devices: $e');
    }
  }

  @override
  void dispose() {
    FlutterBluetoothSerial.instance.setPairingRequestHandler(null);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat Demo'),
      ),
      body: Container(
        child: ListView(
          children: <Widget>[
            Divider(),
            ListTile(
              title: Text('Device: ${_device.name ?? '...'}'),
            ),
            ListTile(
              title: ElevatedButton(
                child: const Text('Check Status'),
                onPressed: () async {
                  print('Connect -> selected ' + _device.address);
                  // _startChat(context, _device);
                  _startApp(context, _device);
                                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _startApp(BuildContext context, BluetoothDevice server) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) {
          return AppPage(server: server);
        },
      ),
    );
  }

  void _startChat(BuildContext context, BluetoothDevice server) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) {
          return ChatPage(server: server);
        },
      ),
    );
  }
}

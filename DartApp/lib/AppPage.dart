// Base application https://github.com/rickyhh2/flutter_rpi_bluetooth_client
// some portions of code developed by ChatGPT and modified accordingly

import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:fl_chart/fl_chart.dart';

class AppPage extends StatefulWidget {
  final BluetoothDevice server;

  const AppPage({required this.server});

  @override
  _AppPage createState() => new _AppPage();
}


class _AppPage extends State<AppPage> {
  late BluetoothConnection connection;

  String message = "";


  bool isConnecting = true;
  bool get isConnected => connection.isConnected;

  bool isDisconnecting = false;

  @override
  void initState() {
    super.initState();
    _initializeConnection();
  }

/// Connect to the Bluetooth device
  void _initializeConnection() {
    BluetoothConnection.toAddress(widget.server.address).then((_connection) {
      print('Connected to the device');
      connection = _connection;
      setState(() {
        isConnecting = false;
        isDisconnecting = false;
      });

      // Listening for incoming data
      connection.input?.listen(_onDataReceived).onDone(() {
        if (isDisconnecting) {
          print('Disconnecting locally!');
        } else {
          print('Disconnected remotely!');
        }
        if (this.mounted) {
          setState(() {});
        }
      });
    }).catchError((error) {
      print('Cannot connect, exception occurred');
      print(error);
    });
  }
  

  @override
  void dispose() {
    // Avoid memory leak (`setState` after dispose) and disconnect
    if (isConnected) {
      isDisconnecting = true;
      connection.dispose();
    }

    super.dispose();
  }

  List<double> rawData = [1.5, 2.2, 3.8, 2.5, 4.0, 3.2, 5.5, 6.8, 5.1, 7.3]; // Sample raw data
  List<double> rawDataInit = [1.5, 2.2, 3.8, 2.5, 4.0, 3.2, 5.5, 6.8, 5.1, 7.3]; // Sample raw data
  List<DataPoint> dataPoints = []; // List to store parsed DataPoints
  DataPoint dummyDataPoint = new DataPoint(timestamp: DateTime.now(), value: 16184.6);
  bool receiving = false;

  void _addRandomData() {
    // Adds random data to the chart and updates the state
    setState(() {
      rawData.add((5 + (5 * (rawData.length % 2 == 0 ? -1 : 1))) * (rawData.length % 1.5)); 
    });
  }

  void _resetData() {
    // Resets the graph data
    setState(() {
      rawData = rawDataInit; 
    });
  }

  @override
  Widget build(BuildContext context) {
    double minXRaw = dataPoints.isNotEmpty 
      ? dataPoints.map((point) => point.timestamp.millisecondsSinceEpoch.toDouble()).reduce((a, b) => a < b ? a : b) 
      : 0;

    double maxXRaw = dataPoints.isNotEmpty 
      ? dataPoints.map((point) => point.timestamp.millisecondsSinceEpoch.toDouble()).reduce((a, b) => a > b ? a : b) 
      : 1000;

    double minYRaw = dataPoints.isNotEmpty 
      ? dataPoints.map((point) => point.value).reduce((a, b) => a < b ? a : b) 
      : 0;

    double maxYRaw = dataPoints.isNotEmpty 
      ? dataPoints.map((point) => point.value).reduce((a, b) => a > b ? a : b) 
      : 10;

    // Prevent divide-by-zero if minX == maxX or minY == maxY
    if (minXRaw == maxXRaw) maxXRaw = minXRaw + 1;
    if (maxYRaw == minYRaw) minYRaw = maxYRaw + 1;
    return Scaffold(
      appBar: AppBar(
        title: Text('Wetness Sensor Data'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: LineChart(
                LineChartData(
                  lineBarsData: [
                    LineChartBarData(
                      spots: dataPoints.map((point) {
                        // X-axis: Timestamp in milliseconds
                        double x = point.timestamp.millisecondsSinceEpoch.toDouble();
                        // Y-axis: The value from DataPoint
                        double y = point.value;
                        return FlSpot(x, y);
                      }).toList(),
                      isCurved: true,
                      gradient: LinearGradient(
                        colors: [Colors.blue, Colors.blueAccent],
                      ),
                      belowBarData: BarAreaData(
                        show: true,
                        gradient: LinearGradient(
                          colors: [Colors.blue.withOpacity(0.2), Colors.blue.withOpacity(0.1)],
                        ),
                      ),
                      barWidth: 3,
                      isStrokeCapRound: true,
                    ),
                  ],
                  minX: minXRaw,
                  maxX: maxXRaw,
                  minY: minYRaw - ((maxYRaw - minYRaw)/5),
                  maxY: maxYRaw + ((maxYRaw - minYRaw)/5),
                  titlesData: FlTitlesData(
                    topTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false), // Disable top labels
                    ),
                    rightTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: false), // Disable right labels
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 50,
                        interval: (maxYRaw - minYRaw) / 5,
                        getTitlesWidget: (double value, TitleMeta meta) {
                          return Text(value.toStringAsFixed(0), style: TextStyle(fontSize: 10));
                        },
                      ),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 40, 
                        interval: (maxXRaw - minXRaw) / 3,
                        getTitlesWidget: (double value, TitleMeta meta) {
                          DateTime date = DateTime.fromMillisecondsSinceEpoch(value.toInt());
                          return SideTitleWidget(
                            axisSide: meta.axisSide,
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Text('${date.month}/${date.day}', style: TextStyle(fontSize: 10)),
                                Text('${date.hour}:${date.minute.toString().padLeft(2, '0')}', style: TextStyle(fontSize: 10)),
                              ],
                            ),
                          );
                        },
                      ),
                    ),
                  ),
                  gridData: FlGridData(
                    show: true,
                    horizontalInterval: ((maxYRaw - minYRaw)/5), // Control the space between Y-axis grid lines
                  ),
                  borderData: FlBorderData(
                    show: true,
                    border: Border(
                      left: BorderSide(color: Colors.black, width: 2),
                      bottom: BorderSide(color: Colors.black, width: 2),
                    ),
                  ),
                ),
              ),
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: isConnected
                          ? () => _sendMessage("Gain1")
                          : null,
                  child: Text('Gain 1'),
                ),
                ElevatedButton(
                  onPressed: isConnected
                          ? () => _sendMessage("Gain2")
                          : null,
                  child: Text('Gain 2'),
                ),
                ElevatedButton(
                  onPressed: isConnected
                          ? () => _sendMessage("Gain23")
                          : null,
                  child: Text('Gain 2/3'),
                ),
                ElevatedButton(
                  onPressed: isConnected
                          ? () => _sendMessage("Reset")
                          : null,
                  child: Text('Reset Data'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
  void _onDataReceived(Uint8List data) {
    // Allocate buffer for parsed data
    if(receiving == false) {
      dataPoints = [];
      receiving = true;
    }
    
    String receivedData = String.fromCharCodes(data);
    print('Raw Data Received: $receivedData');
    if(receivedData.contains("complete")) {
        receiving = false;
        if(dataPoints.length == 1) {
          dataPoints.add(dummyDataPoint);
        }
    }
    else {
      try {
        // Parse the received data into DataPoint objects
        List<dynamic> parsedData = jsonDecode(receivedData);

        // Convert each inner list to a DataPoint object
        List<DataPoint> newPoints = parsedData.map((item) => DataPoint.fromList(item)).toList();

        // Update the state with new data points
        setState(() {
          dataPoints.addAll(newPoints);
        });

        print('Parsed Data Points: $newPoints');
        
      } catch (e) {
        print('Error parsing data: $e');
      }
    }
  }

  void _sendMessage(String text) async {
    text = text.trim();

    if (text.length > 0) {
      try {
        connection.output.add(utf8.encode(text + "\r\n"));
        await connection.output.allSent;

      } catch (e) {
        // Ignore error, but notify state
        setState(() {});
      }
    }
  }
}

class DataPoint {
  final DateTime timestamp;
  final double value;

  DataPoint({required this.timestamp, required this.value});

  // Factory method to create a DataPoint from a list
  factory DataPoint.fromList(List<dynamic> data) {
    return DataPoint(
      timestamp: DateTime.parse(data[0]),
      value: data[1] as double,
    );
  }

  @override
  String toString() {
    return 'DataPoint(timestamp: $timestamp, value: $value)';
  }
}


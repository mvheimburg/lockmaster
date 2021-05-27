import 'dart:async';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_browser_client.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'dart:convert' show json;

// final client = MqttBrowserClient('mqtt://192.168.1.2', '');
class MqttParams {
  late final String clientId;
  late final String broker;
  late final String port;
  late final String password;
  late final String username;

  MqttParams(
      {this.clientId = "",
      this.broker = "",
      this.port = "",
      this.password = "",
      this.username = ""});

  factory MqttParams.fromJson(Map<String, dynamic> jsonMap) {
    return new MqttParams(
        clientId: jsonMap["MQTT_CLIENT_ID"],
        broker: jsonMap["MQTT_BROKER"],
        port: jsonMap["MQTT_PORT"],
        password: jsonMap["MQTT_PASSWORD"],
        username: jsonMap["MQTT_USERNAME"]);
  }
}

class MqttService {
  // final String apiUrl = "/doormanager";

  // final String buildType = 'dev';
  final String mqttParamsPath = "mqtt_secrets.json";
  late Future<MqttBrowserClient> client;

  // final String apiKey = (Map<String, dynamic> jsonMap) {
  //   return new Secret(apiKey: jsonMap["api_key"]);
  // }

  MqttService() {
    client = this.connect();
  }

  Future<MqttParams> load() {
    return rootBundle.loadStructuredData<MqttParams>(this.mqttParamsPath,
        (jsonStr) async {
      final secret = MqttParams.fromJson(json.decode(jsonStr));
      return secret;
    });
  }

  Future<MqttBrowserClient> connect() async {
    MqttParams mqttParams = await load();
    print(mqttParams.port);
    MqttBrowserClient client = MqttBrowserClient.withPort(
        mqttParams.broker, mqttParams.clientId, int.parse(mqttParams.port));
    client.logging(on: true);
    client.onConnected = onConnected;
    client.onDisconnected = onDisconnected;
    client.onSubscribed = onSubscribed;
    client.onSubscribeFail = onSubscribeFail;
    client.pongCallback = pong;

    final connMessage = MqttConnectMessage()
        .withClientIdentifier(mqttParams.clientId)
        .authenticateAs(mqttParams.username, mqttParams.password)
        .withWillTopic('willtopic')
        .withWillMessage('willMessage')
        .startClean()
        .withWillQos(MqttQos.atLeastOnce);
    client.connectionMessage = connMessage;
    try {
      await client.connect();
    } catch (e) {
      print('Exception: $e');
      client.disconnect();
    }

    return client;
  }

  void ringDoorbell() {
    String topic = "bell/ring/toggle";
    final builder = MqttClientPayloadBuilder();
    builder.addString("do");
    // print('EXAMPLE:: <<<< PUBLISH 1 >>>>');
    // client.publishMessage(topic, MqttQos.atLeastOnce, builder1.payload!);
    this.client.then((mqttc) {
      mqttc.publishMessage(topic, MqttQos.atLeastOnce, builder.payload!);
    });
    print('ringDoorbell');
  }

  void onConnected() {
    print('Connected');
  }

  // unconnected
  void onDisconnected() {
    print('Disconnected');
  }

  // subscribe to topic succeeded
  void onSubscribed(String topic) {
    print('Subscribed topic: $topic');
  }

  // subscribe to topic failed
  void onSubscribeFail(String topic) {
    print('Failed to subscribe $topic');
  }

  // unsubscribe succeeded
  void onUnsubscribed(String topic) {
    print('Unsubscribed topic: $topic');
  }

  // PING response received
  void pong() {
    print('Ping response client callback invoked');
  }
}

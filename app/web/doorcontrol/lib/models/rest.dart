import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class User {
  final int? id;
  final String name;
  final int? pin;
  final String? mac;
  final String? start;
  final String? end;
  final int accessLevel;

  User(
      {this.id,
      required this.name,
      this.pin,
      this.mac,
      this.start,
      this.end,
      required this.accessLevel});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
        id: json['id'],
        name: json['name'],
        pin: json['pin'],
        mac: json['mac'],
        start: json['start'],
        end: json['end'],
        accessLevel: json['access_level']);
  }
}

class Candidate {
  final String mac;
  final int rssi;

  Candidate({required this.mac, required this.rssi});

  factory Candidate.fromJson(Map<String, dynamic> json) {
    return Candidate(mac: json['mac'], rssi: json['rssi']);
  }
}

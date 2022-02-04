import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class User {
  final int? id;
  final String name;
  final int? pin;
  final String? uuid;
  final String? start;
  final String? end;
  final int accessLevel;

  User(
      {this.id,
      required this.name,
      this.pin,
      this.uuid,
      this.start,
      this.end,
      required this.accessLevel});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
        id: json['id'],
        name: json['name'],
        pin: json['pin'],
        uuid: json['uuid'],
        start: json['start'],
        end: json['end'],
        accessLevel: json['access_level']);
  }
}

// class Candidate {
//   final String uuid;

//   Candidate({required this.uuid});

//   factory Candidate.fromJson(Map<String, dynamic> uuid) {
//     return Candidate(uuid: uuid);
//   }
// }

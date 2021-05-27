import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Access {
  final int accessLevel;

  Access({required this.accessLevel});

  factory Access.fromJson(Map<String, dynamic> json) {
    return Access(accessLevel: json['access_level']);
  }
}

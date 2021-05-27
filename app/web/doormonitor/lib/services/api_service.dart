import 'dart:convert';
// import 'dart:io';

// import 'package:Doormonitor/models/rest.dart';
import 'package:http/http.dart' as http;
// import 'package:flutter/services.dart' show rootBundle;
// import 'dart:convert' show json;
// import 'package:flutter_config/flutter_config.dart';

// class ApiParams {
//   final String apiAddress;

//   ApiParams({required this.apiAddress});

//   factory ApiParams.fromJson(Map<String, dynamic> json) {
//     return ApiParams(apiAddress: json["API_ADDRESS"]);
//   }
// }

// class ApiParamsLoader {
//   final String apiParamsPath = "api_secrets.json";

//   Future<ApiParams> load() {
//     return rootBundle.loadStructuredData<ApiParams>(this.apiParamsPath,
//         (jsonStr) async {
//       final secret = ApiParams.fromJson(json.decode(jsonStr));
//       return secret;
//     });
//   }
// }

class ApiService {
  // final String apiUrl = "/doormanager";
  // final String apiParamsPath = "api_secrets.json";
  late final String apiUrl = "http://192.168.1.100/doormanager";
  // late Future<ApiParams> apiParams;
  //
  // ApiService._(this.buildType, this.apiUrl);
  ApiService() {
    // apiUrl = FlutterConfig.get('API_ADDRESS');
    // print('apiUrl: $apiUrl');
    // apiParams = this.load();
  }

  // Future<ApiParams> load() {
  //   print("loading api params");
  //   return rootBundle.loadStructuredData<ApiParams>(this.apiParamsPath,
  //       (jsonStr) async {
  //     final secret = ApiParams.fromJson(json.decode(jsonStr));
  //     print(secret);
  //     return secret;
  //   });
  // }

  Future<int> getAccessLevel() async {
    final http.Response response =
        await http.get(Uri.parse("$apiUrl/get_access_level"));

    if (response.statusCode == 200) {
      int access = json.decode(response.body);
      return access;
    } else {
      throw "Failed to load Access";
    }
  }

  // Future<int> getAccessLevel() async {
  //   apiParams.then((ApiParams params) async {
  //     print('ringing bell at: ${params.apiAddress}');
  //     final http.Response response =
  //         await http.get(Uri.parse("${params.apiAddress}/get_access_level"));

  //     if (response.statusCode == 200) {
  //       int access = json.decode(response.body);
  //       return access;
  //     } else {
  //       throw "Failed to load Access";
  //     }
  //   }, onError: throw "Api address not loaded");
  // }

  // Future<int> ringDoorbell() async {
  //   http.Response response = await http
  //       .post(Uri.parse("$apiUrl/ring_doorbell"), headers: <String, String>{
  //     'Content-Type': 'application/json; charset=UTF-8',
  //   });

  //   if (response.statusCode == 201) {
  //     return json.decode(response.body);
  //   } else {
  //     throw Exception('Failed to post User');
  //   }
  // }
}

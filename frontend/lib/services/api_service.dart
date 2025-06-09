// frontend/lib/services/api_service.dart

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auth_service.dart';

class ApiService {
  final AuthService _authService;
  static const String _baseUrl = 'http://127.0.0.1:8000/api/v1';

  // The constructor now requires the AuthService instance to be passed in.
  ApiService(this._authService);

  // A private helper method to create authenticated headers.
  Future<Map<String, String>> _getHeaders({bool isFormData = false}) async {
    final token = await _authService.getToken();
    return {
      if (!isFormData) 'Content-Type': 'application/json; charset=UTF-8',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // A generic POST method that automatically adds the auth token for JSON data.
  Future<http.Response> post(String path, Map<String, dynamic> data) async {
    final headers = await _getHeaders();
    final url = Uri.parse('$_baseUrl$path');
    final body = json.encode(data);
    
    return http.post(url, headers: headers, body: body);
  }

  // A specific POST for URL-encoded data (used for login).
  Future<http.Response> postUrlEncoded(String path, Map<String, String> data) async {
    final url = Uri.parse('$_baseUrl$path');
    return http.post(url, body: data);
  }
}
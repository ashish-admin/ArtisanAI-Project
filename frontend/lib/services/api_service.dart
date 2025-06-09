// frontend/lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auth_service.dart';

class ApiService {
  final String _baseUrl = 'http://127.0.0.1:8000/api/v1';
  final AuthService _authService;

  // The AuthService is now injected via the constructor.
  ApiService(this._authService);

  Future<Map<String, String>> _getHeaders() async {
    // It now uses the single, app-wide instance of AuthService to get the token.
    final token = await _authService.getToken();
    if (token == null) {
      throw Exception('Not authenticated. Please log in.');
    }
    return {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer $token',
    };
  }

  Future<List<dynamic>> getConfigurations() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/configurations/'),
      headers: await _getHeaders(),
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load configurations');
    }
  }

  Future<void> deleteConfiguration(int id) async {
    final response = await http.delete(
      Uri.parse('$_baseUrl/configurations/$id'),
      headers: await _getHeaders(),
    );
    if (response.statusCode != 204) {
      throw Exception('Failed to delete configuration.');
    }
  }

  Future<Map<String, dynamic>> refinePromptWithAgent(String prompt) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/agent/refine-prompt'),
      headers: await _getHeaders(),
      body: jsonEncode(<String, String>{'prompt': prompt}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      print('Failed to refine prompt: ${response.statusCode} ${response.body}');
      throw Exception('Failed to refine prompt');
    }
  }

  Future<Map<String, dynamic>> getLlmSuggestions(String prompt) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/llm-suggestions/'),
      headers: await _getHeaders(),
      body: jsonEncode(<String, String>{'prompt': prompt}),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      print('Failed to get LLM suggestions: ${response.statusCode} ${response.body}');
      throw Exception('Failed to get LLM suggestions');
    }
  }
}
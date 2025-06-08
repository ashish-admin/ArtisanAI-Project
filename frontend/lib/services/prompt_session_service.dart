// lib/services/prompt_session_service.dart
import 'package:flutter/foundation.dart';

// A simple data class to hold all the pieces of a prompt configuration.
class PromptData {
  String userGoal;
  String selectedOutputFormat;
  String contextProvided;
  Map<String, dynamic> constraints;
  String personaDescription;
  bool personaSkipped;

  PromptData({
    this.userGoal = '',
    this.selectedOutputFormat = '',
    this.contextProvided = '',
    Map<String, dynamic>? constraints,
    this.personaDescription = '',
    this.personaSkipped = false,
  }) : constraints = constraints ?? {'prioritizeQuality': true}; // Ensure constraints map is never null
}

class PromptSessionService with ChangeNotifier {
  PromptData _sessionData = PromptData();

  PromptData get sessionData => _sessionData;

  /// Loads the session with data from a saved configuration.
  void loadSession(Map<String, dynamic> savedConfig) {
    _sessionData = PromptData(
      userGoal: savedConfig['userGoal'] ?? '',
      selectedOutputFormat: savedConfig['selectedOutputFormat'] ?? '',
      contextProvided: savedConfig['contextProvided'] ?? '',
      constraints: Map<String, dynamic>.from(savedConfig['constraints'] ?? {'prioritizeQuality': true}),
      personaDescription: savedConfig['personaDescription'] ?? '',
      personaSkipped: savedConfig['personaSkipped'] ?? false,
    );
    if (kDebugMode) {
      print("PromptSessionService: Session loaded with configuration named '${savedConfig['name']}'.");
    }
    // We don't notify listeners here, as navigation will trigger the UI update.
  }

  /// Clears the session to start a new prompt from scratch.
  void clearSession() {
    _sessionData = PromptData();
    if (kDebugMode) {
      print("PromptSessionService: Session cleared for new prompt.");
    }
    // We might not need to notify here if the user is always navigated away immediately after.
    // However, it's safer to leave it in.
    notifyListeners();
  }

  // Individual methods to update the session state from each screen.
  void updateUserGoal(String goal) {
    _sessionData.userGoal = goal;
    // No need to notify for intermediate steps
  }

  void updateOutputFormat(String format) {
    _sessionData.selectedOutputFormat = format;
  }

  void updateContext(String context) {
    _sessionData.contextProvided = context;
  }
  
  void updateConstraints(Map<String, dynamic> newConstraints) {
    _sessionData.constraints = newConstraints;
  }

  void updatePersona(String description, bool skipped) {
    _sessionData.personaDescription = description;
    _sessionData.personaSkipped = skipped;
  }
}
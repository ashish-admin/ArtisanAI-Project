// frontend/lib/services/prompt_session_service.dart
import 'package:flutter/foundation.dart';

class PromptSessionService with ChangeNotifier {
  String? _goal;
  String? _outputFormat;
  String? _context;
  String? _constraints;
  String? _personaDescription;
  bool _personaSkipped = false;

  String? get goal => _goal;
  String? get outputFormat => _outputFormat;
  String? get context => _context;
  String? get constraints => _constraints;
  String? get personaDescription => _personaDescription;
  bool get personaSkipped => _personaSkipped;

  void setGoal(String goal) {
    _goal = goal;
    notifyListeners();
  }

  void setOutputFormat(String format) {
    _outputFormat = format;
    notifyListeners();
  }

  void setContext(String? context) {
    _context = context;
    notifyListeners();
  }

  void setConstraints(String? constraints) {
    _constraints = constraints;
    notifyListeners();
  }

  void setPersona({String? description, bool skipped = false}) {
    _personaDescription = description;
    _personaSkipped = skipped;
    notifyListeners();
  }

  void resetSession() {
    _goal = null;
    _outputFormat = null;
    _context = null;
    _constraints = null;
    _personaDescription = null;
    _personaSkipped = false;
    notifyListeners();
  }

  String getFinalPrompt() {
    final parts = <String>[];
    if (_goal != null && _goal!.isNotEmpty) {
      parts.add('### Goal\n$_goal');
    }
    if (_outputFormat != null && _outputFormat!.isNotEmpty) {
      parts.add('### Output Format\n$_outputFormat');
    }
    if (_context != null && _context!.isNotEmpty) {
      parts.add('### Context\n$_context');
    }
    if (_constraints != null && _constraints!.isNotEmpty) {
      parts.add('### Constraints\n$_constraints');
    }
    if (!_personaSkipped && _personaDescription != null && _personaDescription!.isNotEmpty) {
      parts.add('### Persona\n$_personaDescription');
    }
    return parts.join('\n\n---\n\n');
  }
}
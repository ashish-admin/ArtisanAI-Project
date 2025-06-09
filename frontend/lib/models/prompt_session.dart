// frontend/lib/models/prompt_session.dart

class PromptSession {
  String goal = '';
  String format = '';
  String context = '';
  List<String> constraints = [];
  String persona = '';

  PromptSession({
    this.goal = '',
    this.format = '',
    this.context = '',
    this.constraints = const [],
    this.persona = '',
  });

  Map<String, dynamic> toJson() {
    return {
      'goal': goal,
      'format': format,
      'context': context,
      'constraints': constraints,
      'persona': persona,
    };
  }
}
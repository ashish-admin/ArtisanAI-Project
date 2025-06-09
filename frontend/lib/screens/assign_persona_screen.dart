// frontend/lib/screens/assign_persona_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/prompt_session_service.dart';
import 'review_prompt_screen.dart';

class AssignPersonaScreen extends StatefulWidget {
  // The constructor no longer takes individual parameters
  const AssignPersonaScreen({super.key});

  @override
  State<AssignPersonaScreen> createState() => _AssignPersonaScreenState();
}

class _AssignPersonaScreenState extends State<AssignPersonaScreen> {
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    final session = Provider.of<PromptSessionService>(context, listen: false);
    if (!session.personaSkipped) {
      _controller.text = session.personaDescription ?? '';
    }
  }

  void _onNext({bool skipped = false}) {
    final sessionService = Provider.of<PromptSessionService>(context, listen: false);
    sessionService.setPersona(
      description: skipped ? null : _controller.text,
      skipped: skipped,
    );

    Navigator.of(context).push(
      MaterialPageRoute(
        // Pass the single sessionService instance to the next screen
        builder: (context) => ReviewPromptScreen(sessionService: sessionService),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Step 5: Assign a Persona')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text(
              'Describe the persona the AI should adopt.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'e.g., "A helpful and friendly assistant..."',
              ),
              maxLines: 5,
            ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                TextButton(
                  onPressed: () => _onNext(skipped: true),
                  child: const Text('Skip'),
                ),
                ElevatedButton(
                  onPressed: _onNext,
                  child: const Text('Review Prompt'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class AssignPersonaScreen extends StatelessWidget {
  const AssignPersonaScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final personaController = TextEditingController();
    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 5: Assign a Persona'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Define the persona the AI should adopt.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: personaController,
              decoration: const InputDecoration(
                labelText: 'e.g., "A skeptical editor", "An enthusiastic fan"',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.multiline,
              maxLines: null,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                if (personaController.text.isNotEmpty) {
                  Provider.of<PromptSessionService>(context, listen: false)
                      .updatePersona(personaController.text);
                  Navigator.pushNamed(context, '/review'); // Use named route
                }
              },
              child: const Text('Review & Refine'),
            ),
          ],
        ),
      ),
    );
  }
}
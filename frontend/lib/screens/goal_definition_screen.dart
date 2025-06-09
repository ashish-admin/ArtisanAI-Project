import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class GoalDefinitionScreen extends StatelessWidget {
  const GoalDefinitionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final goalController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 1: Define Your Goal'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'What is your primary objective?',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: goalController,
              decoration: const InputDecoration(
                labelText: 'e.g., "Critique a chapter"',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.multiline,
              maxLines: null,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                if (goalController.text.isNotEmpty) {
                  Provider.of<PromptSessionService>(context, listen: false)
                      .updateGoal(goalController.text);
                  Navigator.pushNamed(context, '/format'); // Use named route
                }
              },
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}
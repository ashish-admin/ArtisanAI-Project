import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class DefineConstraintsScreen extends StatelessWidget {
  const DefineConstraintsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final constraintsController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 4: Set Constraints'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Set parameters like length, tone, keywords, etc. (comma-separated).',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: constraintsController,
              decoration: const InputDecoration(
                labelText: 'e.g., "formal, under 500 words"',
                border: OutlineInputBorder(),
              ),
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                final constraints = constraintsController.text
                    .split(',')
                    .map((e) => e.trim())
                    .where((e) => e.isNotEmpty)
                    .toList();
                Provider.of<PromptSessionService>(context, listen: false)
                    .updateConstraints(constraints);
                Navigator.pushNamed(context, '/persona'); // Use named route
              },
              child: const Text('Next'),
            ),
          ],
        ),
      ),
    );
  }
}
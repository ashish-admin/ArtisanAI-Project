import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class SpecifyOutputScreen extends StatelessWidget {
  const SpecifyOutputScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final formatController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 2: Specify Output Format'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Select the desired output structure.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: formatController,
              decoration: const InputDecoration(
                labelText: 'e.g., "Email", "JSON"',
                border: OutlineInputBorder(),
              ),
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: () {
                if (formatController.text.isNotEmpty) {
                  Provider.of<PromptSessionService>(context, listen: false)
                      .updateFormat(formatController.text);
                  Navigator.pushNamed(context, '/context'); // Use named route
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
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:artisan_ai/services/prompt_session_service.dart';

class ProvideContextScreen extends StatelessWidget {
  const ProvideContextScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final contextController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Step 3: Provide Context'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Provide the essential background information or text to be critiqued.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: TextField(
                controller: contextController,
                decoration: const InputDecoration(
                  labelText: 'Paste your text here...',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.multiline,
                maxLines: null,
                expands: true,
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                if (contextController.text.isNotEmpty) {
                  Provider.of<PromptSessionService>(context, listen: false)
                      .updateContext(contextController.text);
                  Navigator.pushNamed(context, '/constraints'); // Use named route
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
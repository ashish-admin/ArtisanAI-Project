// frontend/lib/screens/specify_output_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/prompt_session_service.dart';
import 'provide_context_screen.dart';

class SpecifyOutputScreen extends StatefulWidget {
  const SpecifyOutputScreen({super.key});

  @override
  State<SpecifyOutputScreen> createState() => _SpecifyOutputScreenState();
}

class _SpecifyOutputScreenState extends State<SpecifyOutputScreen> {
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Pre-fill with existing data.
    _controller.text = Provider.of<PromptSessionService>(context, listen: false).outputFormat ?? '';
  }

  void _onNext() {
    if (_controller.text.isNotEmpty) {
      // Save data to the service.
      Provider.of<PromptSessionService>(context, listen: false)
          .setOutputFormat(_controller.text);
          
      // Corrected: Navigate without any invalid parameters.
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => const ProvideContextScreen(),
        ),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Step 2: Specify Output Format')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Describe the desired output format.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'e.g., "A JSON object with keys: subject, body, closing"...',
              ),
              maxLines: 5,
            ),
            const Spacer(),
            ElevatedButton(
              onPressed: _onNext,
              child: const Text('Next'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
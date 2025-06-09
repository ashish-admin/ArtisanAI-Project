// frontend/lib/screens/provide_context_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/prompt_session_service.dart';
import 'define_constraints_screen.dart';

class ProvideContextScreen extends StatefulWidget {
  const ProvideContextScreen({super.key});

  @override
  State<ProvideContextScreen> createState() => _ProvideContextScreenState();
}

class _ProvideContextScreenState extends State<ProvideContextScreen> {
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Pre-fill with existing data.
    _controller.text = Provider.of<PromptSessionService>(context, listen: false).context ?? '';
  }

  void _onNext({bool skipped = false}) {
    // Save data to the service.
    Provider.of<PromptSessionService>(context, listen: false)
        .setContext(skipped ? null : _controller.text);
    // Navigate cleanly.
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => const DefineConstraintsScreen(),
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
      appBar: AppBar(title: const Text('Step 3: Provide Context (Optional)')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Provide any relevant context, examples, or background information.',
              style: TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'e.g., "The target audience is tech professionals..."',
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
                  child: const Text('Next'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app_state.dart';
import 'models.dart';

class ClipCard extends StatelessWidget {
  const ClipCard({super.key, required this.hit, required this.state, this.onPin});

  final SearchHit hit;
  final AppState state;
  final VoidCallback? onPin;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(hit.question, style: const TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Text(hit.answer, style: const TextStyle(color: Colors.white70, height: 1.4)),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                if (hit.timestampUrl.isNotEmpty)
                  FilledButton(
                    onPressed: () => state.openUrl(hit.timestampUrl),
                    child: Text(state.t('क्लिप देखें', 'Watch clip')),
                  ),
                if (onPin != null)
                  OutlinedButton(
                    onPressed: onPin,
                    child: Text(state.t('पिन', 'Pin')),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class JapaOrb extends StatefulWidget {
  const JapaOrb({super.key, required this.state, this.onAsk});

  final AppState state;
  final VoidCallback? onAsk;

  @override
  State<JapaOrb> createState() => _JapaOrbState();
}

class _JapaOrbState extends State<JapaOrb> {
  Timer? _hold;
  bool _openedAsk = false;

  @override
  void dispose() {
    _hold?.cancel();
    super.dispose();
  }

  void _down(TapDownDetails _) {
    _openedAsk = false;
    _hold?.cancel();
    _hold = Timer(const Duration(milliseconds: 2500), () {
      _openedAsk = true;
      HapticFeedback.mediumImpact();
      widget.onAsk?.call();
    });
  }

  void _up(TapUpDetails _) {
    _hold?.cancel();
    if (!_openedAsk) {
      HapticFeedback.lightImpact();
      widget.state.tapBead();
    }
  }

  void _cancel() {
    _hold?.cancel();
  }

  @override
  Widget build(BuildContext context) {
    final mala = widget.state.mala;
    return Positioned(
      right: 16,
      bottom: 24,
      child: GestureDetector(
        onTapDown: _down,
        onTapUp: _up,
        onTapCancel: _cancel,
        child: Material(
          elevation: 8,
          color: const Color(0xFF2A2A2A),
          shape: const CircleBorder(),
          child: SizedBox(
            width: 88,
            height: 88,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  '${mala.currentInCycle}',
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                ),
                Text(widget.state.t('माला', 'Mala'), style: const TextStyle(fontSize: 11, color: Colors.white70)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class StatCard extends StatelessWidget {
  const StatCard({super.key, required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 150,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            children: [
              Text(value, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
              Text(label, style: const TextStyle(color: Colors.white70)),
            ],
          ),
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'app_state.dart';
import 'models.dart';
import 'widgets.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key, required this.state});
  final AppState state;

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  final _history = <String>[];
  AskResult? _result;
  bool _loading = false;

  Future<void> _send([String? text]) async {
    final query = (text ?? _controller.text).trim();
    if (query.isEmpty) return;
    setState(() => _loading = true);
    try {
      final result = await widget.state.ask(query, _history);
      _history.add(query);
      _controller.clear();
      if (!mounted) return;
      setState(() => _result = result);
    } catch (err) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$err')));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = widget.state;
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 120),
      children: [
        Text(state.t('प्रवचन से पूछें', 'Ask from the discourses'), style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        Text(
          state.t('उत्तर केवल वीडियो से। होल्ड = पूछें।', 'Answers only from videos. Hold the orb to ask.'),
          style: const TextStyle(color: Colors.white70),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _controller,
          minLines: 1,
          maxLines: 3,
          textInputAction: TextInputAction.send,
          onSubmitted: _send,
          decoration: InputDecoration(
            hintText: state.t('प्रश्न लिखें…', 'Type a question…'),
            suffixIcon: IconButton(onPressed: _loading ? null : _send, icon: const Icon(Icons.send)),
          ),
        ),
        if (_loading) const Padding(padding: EdgeInsets.all(24), child: Center(child: CircularProgressIndicator())),
        if (_result != null) ...[
          const SizedBox(height: 16),
          Text(_result!.answer, style: TextStyle(color: _result!.refused ? Colors.amber : Colors.white, height: 1.45)),
          const SizedBox(height: 12),
          ..._result!.clips.map((hit) => Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: ClipCard(
                  hit: hit,
                  state: state,
                  onPin: () => state.pinHit(hit),
                ),
              )),
          if (state.companions.isNotEmpty) ...[
            const SizedBox(height: 16),
            Text(state.t('सार्वजनिक पाठ (वीडियो नहीं)', 'Public texts (not videos)'), style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            ...state.companions.map((card) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: CompanionTile(card: card, state: state),
                )),
          ],
        ],
      ],
    );
  }
}

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key, required this.state});
  final AppState state;

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _controller = TextEditingController();
  List<SearchHit> _hits = const [];
  bool _loading = false;

  Future<void> _run() async {
    final query = _controller.text.trim();
    if (query.isEmpty) return;
    setState(() => _loading = true);
    try {
      final hits = await widget.state.search(query, const []);
      if (!mounted) return;
      setState(() => _hits = hits);
    } catch (err) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$err')));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = widget.state;
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 120),
      children: [
        DropdownButton<String>(
          isExpanded: true,
          value: state.channels.any((channel) => channel.id == state.channelId)
              ? state.channelId
              : (state.channels.isEmpty ? 'all' : state.channels.first.id),
          items: (state.channels.isEmpty
                  ? const [ChannelItem(id: 'all', name: 'All', nameHi: 'सभी')]
                  : state.channels)
              .map(
                (channel) => DropdownMenuItem(
                  value: channel.id,
                  child: Text(state.isHindi ? channel.nameHi : channel.name),
                ),
              )
              .toList(),
          onChanged: (value) {
            if (value != null) state.setChannel(value);
          },
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _controller,
          onSubmitted: (_) => _run(),
          decoration: InputDecoration(
            hintText: state.t('खोजें…', 'Search…'),
            suffixIcon: IconButton(onPressed: _loading ? null : _run, icon: const Icon(Icons.search)),
          ),
        ),
        if (_loading) const Padding(padding: EdgeInsets.all(24), child: Center(child: CircularProgressIndicator())),
        const SizedBox(height: 12),
        ..._hits.map((hit) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: ClipCard(hit: hit, state: state, onPin: () => state.pinHit(hit)),
            )),
      ],
    );
  }
}

class SadhanaScreen extends StatelessWidget {
  const SadhanaScreen({super.key, required this.state});
  final AppState state;

  @override
  Widget build(BuildContext context) {
    final mala = state.mala;
    final percent = mala.beadsPerCycle == 0 ? 0.0 : mala.currentInCycle / mala.beadsPerCycle;
    final named = state.dashboard?.namedMalas ?? const [];
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 120),
      children: [
        Text(state.t('साधना', 'Sadhana'), style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 16),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            StatCard(label: state.t('मनके', 'Beads'), value: '${mala.beadsToday}'),
            StatCard(label: state.t('माला', 'Malas'), value: '${mala.cyclesToday}'),
            StatCard(label: state.t('चक्र', 'Cycle'), value: '${mala.currentInCycle}/${mala.beadsPerCycle}'),
            StatCard(label: state.t('प्रश्न', 'Questions'), value: '${mala.questionsToday}'),
          ],
        ),
        const SizedBox(height: 16),
        LinearProgressIndicator(value: percent.clamp(0, 1)),
        const SizedBox(height: 16),
        if (named.isNotEmpty) ...[
          Text(state.t('नामित माला', 'Named mala'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: named
                .map(
                  (item) => ChoiceChip(
                    label: Text(item.label(state.isHindi)),
                    selected: mala.mantraId == item.id,
                    onSelected: (_) => state.updateControl({'mantra_id': item.id}),
                  ),
                )
                .toList(),
          ),
          const SizedBox(height: 16),
        ],
        FilledButton(onPressed: state.tapBead, child: Text(state.t('मनका', 'Bead'))),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: () {
            HapticFeedback.selectionClick();
            state.undoBead();
          },
          child: Text(state.t('वापस', 'Undo')),
        ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: state.toggleOverlay,
          child: Text(
            state.overlayOn
                ? state.t('ओवरले बंद', 'Hide overlay')
                : state.t('ओवरले', 'Overlay bubble'),
          ),
        ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: state.toggleLiveActivity,
          child: Text(state.t('लाइव गतिविधि', 'Live Activity')),
        ),
        const SizedBox(height: 8),
        OutlinedButton(
          onPressed: state.toggleWatch,
          child: Text(state.t('घड़ी', 'Watch')),
        ),
        if (state.today?.gita != null) ...[
          const SizedBox(height: 24),
          Text(state.t('आज का श्लोक', "Today's verse"), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          CompanionTile(card: state.today!.gita!, state: state),
        ],
        if (state.today?.sandhya != null) ...[
          const SizedBox(height: 12),
          CompanionTile(card: state.today!.sandhya!, state: state),
        ],
      ],
    );
  }
}

class ControlDashboardScreen extends StatelessWidget {
  const ControlDashboardScreen({super.key, required this.state});
  final AppState state;

  Future<void> _run(BuildContext context, Future<void> Function() action) async {
    try {
      await action();
    } catch (err) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$err')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final dash = state.dashboard;
    final stats = dash?.stats ?? const {};
    final controls = dash?.controls ?? const {};
    final dbOk = asBool(state.health?['database']);
    return RefreshIndicator(
      onRefresh: state.refreshDashboard,
      child: ListView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 120),
        children: [
          Text(state.t('कंट्रोल डैशबोर्ड', 'Control dashboard'), style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 8),
          Text(
            dash?.ready == true ? state.t('API तैयार', 'API ready') : state.t('API कनेक्ट करें', 'Connect the API'),
            style: TextStyle(color: dash?.ready == true ? Colors.greenAccent : Colors.amber),
          ),
          Text(
            dbOk
                ? state.t('डेटाबेस जुड़ा · ${dash?.database ?? 'uttar_sewa'}', 'Database connected · ${dash?.database ?? 'uttar_sewa'}')
                : state.t('डेटाबेस बाद में जुड़ेगा — API फिर भी चलता है', 'Database will connect later — API still runs'),
            style: const TextStyle(color: Colors.white70),
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              StatCard(label: state.t('वीडियो', 'Videos'), value: '${stats['total_videos'] ?? 0}'),
              StatCard(label: state.t('प्रोसेस्ड', 'Processed'), value: '${stats['processed_videos'] ?? 0}'),
              StatCard(label: state.t('Q&A', 'Q&A'), value: '${stats['total_qa_pairs'] ?? 0}'),
              StatCard(label: state.t('पिन', 'Pinned'), value: '${stats['pinned_qa'] ?? 0}'),
            ],
          ),
          const SizedBox(height: 16),
          Text(state.t('माला नियंत्रण', 'Mala controls'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: (dash?.allowedCycles ?? const [11, 27, 54, 108])
                .map(
                  (cycle) => ChoiceChip(
                    label: Text('$cycle'),
                    selected: asInt(controls['beads_per_cycle'], 108) == cycle,
                    onSelected: (_) => state.updateControl({'beads_per_cycle': cycle}),
                  ),
                )
                .toList(),
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 8,
            children: (dash?.namedMalas ?? const [])
                .map(
                  (item) => ChoiceChip(
                    label: Text(item.label(state.isHindi)),
                    selected: controls['mantra_id'] == item.id,
                    onSelected: (_) => state.updateControl({'mantra_id': item.id}),
                  ),
                )
                .toList(),
          ),
          SwitchListTile(
            title: Text(state.t('संध्या', 'Sandhya')),
            value: asBool(controls['sandhya'], true),
            onChanged: (value) => state.updateControl({'sandhya': value}),
          ),
          SwitchListTile(
            title: Text(state.t('जप फोकस', 'Japa focus')),
            value: asBool(controls['japa_focus']),
            onChanged: (value) => state.updateControl({'japa_focus': value}),
          ),
          SwitchListTile(
            title: Text(state.t('प्रोसेसिंग', 'Processing')),
            value: asBool(controls['processing_enabled'], true),
            onChanged: (value) => state.updateControl({'processing_enabled': value}),
          ),
          SwitchListTile(
            title: Text(state.t('सार्वजनिक साथी पाठ', 'Public companion texts')),
            subtitle: Text(state.t('गीता / विकिपीडिया — वीडियो उत्तर नहीं', 'Gita / Wikipedia — not the video answer')),
            value: asBool(controls['public_companions'], true),
            onChanged: (value) => state.updateControl({'public_companions': value}),
          ),
          const SizedBox(height: 8),
          FilledButton(
            onPressed: () => _run(context, () async {
              await state.api.startProcessing();
              await state.refreshDashboard();
            }),
            child: Text(state.t('प्रोसेसिंग शुरू', 'Start processing')),
          ),
          const SizedBox(height: 8),
          OutlinedButton(
            onPressed: () => _run(context, () async {
              final channel = state.channelId == 'all' ? 'bhajanmarg' : state.channelId;
              await state.api.ingestLibrary(channel: channel);
              await state.refreshDashboard();
            }),
            child: Text(state.t('YouTube लाइब्रेरी', 'Ingest YouTube')),
          ),
          const SizedBox(height: 8),
          OutlinedButton(
            onPressed: () => _run(context, () async {
              await state.api.clearProcessing();
              await state.refreshDashboard();
            }),
            child: Text(state.t('स्थिति साफ़ करें', 'Clear status')),
          ),
          const SizedBox(height: 24),
          Text(state.t('पिन किए क्लिप', 'Pinned clips'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          if (state.pinned.isEmpty)
            Text(state.t('अभी कोई पिन नहीं', 'Nothing pinned yet'), style: const TextStyle(color: Colors.white70)),
          ...state.pinned.take(8).map(
                (item) => ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text('${item['question'] ?? ''}'),
                  subtitle: Text('${item['video_title'] ?? item['video_id'] ?? ''}'),
                ),
              ),
          const SizedBox(height: 16),
          Text(state.t('लाइब्रेरी गैप', 'Library gaps'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          if (state.gaps.isEmpty)
            Text(state.t('सभी वीडियो प्रोसेस्ड या सूची खाली', 'All processed, or the list is empty'), style: const TextStyle(color: Colors.white70)),
          ...state.gaps.take(8).map(
                (item) => ListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text('${item['title'] ?? item['video_id'] ?? ''}'),
                  subtitle: Text('${item['video_id'] ?? ''}'),
                ),
              ),
          const SizedBox(height: 16),
          Text(state.t('सार्वजनिक स्रोत', 'Public sources'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          ...state.catalog.map(
            (item) => ListTile(
              contentPadding: EdgeInsets.zero,
              title: Text('${item['name'] ?? item['id'] ?? ''}'),
              subtitle: Text('${item['endpoint'] ?? ''}'),
            ),
          ),
          const SizedBox(height: 8),
          ScrapeBox(state: state),
        ],
      ),
    );
  }
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key, required this.state});
  final AppState state;

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 120),
      children: [
        Text(state.t('सेटिंग्स', 'Settings'), style: Theme.of(context).textTheme.titleLarge),
        SwitchListTile(
          title: Text(state.t('हिंदी', 'Hindi')),
          value: state.isHindi,
          onChanged: (value) => state.setLanguage(value ? 'hi' : 'en'),
        ),
        ListTile(
          title: Text(state.t('API', 'API')),
          subtitle: Text(state.api.baseUrl),
        ),
        ListTile(
          title: Text(state.t('डेटाबेस', 'Database')),
          subtitle: Text(asBool(state.health?['database']) ? 'uttar_sewa' : state.t('ऑफ़लाइन मोड', 'Offline mode')),
        ),
        SwitchListTile(
          title: Text(state.t('सार्वजनिक साथी पाठ', 'Public companion texts')),
          value: asBool(state.dashboard?.controls['public_companions'], true),
          onChanged: (value) => state.updateControl({'public_companions': value}),
        ),
      ],
    );
  }
}

class ScrapeBox extends StatefulWidget {
  const ScrapeBox({super.key, required this.state});
  final AppState state;

  @override
  State<ScrapeBox> createState() => _ScrapeBoxState();
}

class _ScrapeBoxState extends State<ScrapeBox> {
  final _controller = TextEditingController(text: 'https://en.wikipedia.org/wiki/Karma');
  String? _preview;
  bool _loading = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _run() async {
    setState(() => _loading = true);
    try {
      final data = await widget.state.api.scrape(_controller.text.trim());
      if (!mounted) return;
      setState(() => _preview = '${data['title'] ?? ''}\n${data['text'] ?? ''}');
    } catch (err) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$err')));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = widget.state;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextField(
          controller: _controller,
          decoration: InputDecoration(
            hintText: 'https://en.wikipedia.org/wiki/Karma',
            suffixIcon: IconButton(onPressed: _loading ? null : _run, icon: const Icon(Icons.download)),
          ),
        ),
        const SizedBox(height: 8),
        Text(state.t('केवल सार्वजनिक allowlist (विकिपीडिया, गीता, Open Library)', 'Allowlisted public hosts only (Wikipedia, Gita, Open Library)'), style: const TextStyle(color: Colors.white70, fontSize: 12)),
        if (_preview != null) ...[
          const SizedBox(height: 8),
          Text(_preview!, style: const TextStyle(color: Colors.white70, height: 1.4)),
        ],
      ],
    );
  }
}

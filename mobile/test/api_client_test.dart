import 'package:flutter_test/flutter_test.dart';
import 'package:uttar_sewa/api_client.dart';

void main() {
  test('resolveApiBase never returns undefined/api', () {
    expect(resolveApiBase(''), 'http://127.0.0.1:8000/api');
    expect(resolveApiBase('undefined'), 'http://127.0.0.1:8000/api');
    expect(resolveApiBase('null'), 'http://127.0.0.1:8000/api');
    expect(resolveApiBase('https://sewa.example'), 'https://sewa.example/api');
    expect(resolveApiBase('https://sewa.example/api/'), 'https://sewa.example/api');
    expect(resolveApiBase('http://192.168.1.20:8000'), 'http://192.168.1.20:8000/api');
  });

  test('ApiClient.baseUrl is mutable after construction', () {
    final client = ApiClient(baseUrl: 'http://127.0.0.1:8000/api');
    client.baseUrl = resolveApiBase('http://10.0.0.4:8000');
    expect(client.baseUrl, 'http://10.0.0.4:8000/api');
  });
}

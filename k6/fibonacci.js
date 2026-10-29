import http from 'k6/http';
import { check } from 'k6';

const baseUrl = (__ENV.BASE_URL || 'http://api:8000').replace(/\/$/, '');

export const options = {
  vus: Number(__ENV.VUS || 5),
  duration: __ENV.DURATION || '30s',
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500'] },
};

export default function () {
  const response = http.get(`${baseUrl}/fibonacci/100`);
  check(response, {
    'status is 200': (r) => r.status === 200,
    'content type is JSON': (r) => r.headers['Content-Type']?.includes('application/json'),
    'value is correct': (r) => r.json('value') === '354224848179261915075',
  });
}

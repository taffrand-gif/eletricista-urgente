// IndexNow key helper — see cnr/client/src/shared/indexnow.ts for full doc
import indexnowKey from '../../../../indexnow-key.txt?raw';

export function getKey(): string {
  return (indexnowKey || '').trim();
}

export function getSubmitUrl(host: string, urlList: string[]): string {
  const key = getKey();
  const params = new URLSearchParams({
    key,
    host,
    urlList: urlList.join('\n'),
  });
  return `https://api.indexnow.org/indexnow?${params.toString()}`;
}

export const INDEXNOW_KEY = getKey();
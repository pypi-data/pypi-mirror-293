import { main } from './index.js';

export async function lum0xhandler(event) {
  let result;

  if (event.triggerType === 'on-demand') {
    const parameters = event.parameters || {}; // 사용자가 지정한 파라미터
    result = await main(parameters);
  } else {
    const limit = event.limit || 250; // 기본값을 주기적 실행 시 사용하는 경우
    result = await main(limit);
  }

  return {
    statusCode: 200,
    body: JSON.stringify(result),
  };
}

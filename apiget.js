
import common from "../../lib/common/common.js"
const jm = /^#jm查(.*)$/
export class excellen extends plugin {
    constructor() {
        super({
            name: 'ejm',
            dsc: 'example',
            event: 'message',
            priority: 1,
            rule: [{
                    reg: jm,
                    fnc: "Jm"
                },
            ]
        }
        )
    }
    async Jm(e) {
      let tup = "";
      for (let m of e.message) {
          tup += m.text;
      }
      tup = tup.replace(/#jm查/g, "").trim();
  
      // 构造请求URL
      let url = `http://127.0.0.1:8000/jmd?jm=${encodeURIComponent(tup)}`;
  
      try {
          // 发起请求
          let res = await fetch(url);
  
          // 检查请求是否成功
          if (!res || !res.ok) {
              logger.error('[jm] 请求失败');
              return await this.reply('错误，请检查车号或稍后重试！');
          }
  
          // 提取响应体为字符串
          const responseText = await res.text();
  
          // 检查响应体的字节大小
          const bytes = Buffer.byteLength(responseText, "utf8");
          console.log(`图片大小：${bytes}字节`);
          if (bytes >= 31457280) {
              logger.error('图片过大，无法发送');
              return this.reply(`图片过大，发送失败，请自行前往官网：https://18comic.vip/photo/${tup}`)
          }
  
          // 处理响应体内容
          let msg = [segment.image(res.url)]; // 返回的是图片
          const forward = [
            '爱护jm，不要爬这么多本子，jm压力大你bot压力也大，西门',
            `https://18comic.vip/photo/${tup}`
        ];
          forward.push(msg);
          const fmsg = await common.makeForwardMsg(e, forward, `album${tup}`);
          await this.reply(fmsg);
  
          return true; // 返回 true，阻挡消息不再往下
      } catch (err) {
          logger.error(`[jm] 请求失败：${err}`);
          return await this.reply('请求失败，请检查车号或稍后重试！');
      }
  }
}

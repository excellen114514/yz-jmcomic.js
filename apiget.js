
import axios from 'axios';
import { URL } from 'url';
import path from 'path';
import fs from 'fs/promises';
import common from "../../lib/common/common.js"
const jm = /^#jm查(.*)$/
export class excellen extends plugin {
    constructor() {
        super({
            name: 'ejm',
            dsc: 'example',
            event: 'message.private',
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
      let url = `http://43.156.230.21:8000/jmd?jm=${encodeURIComponent(tup)}`;
  
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
              logger.error('图片过大，将请求pdf下载并文件发送');
              let url = `http://43.156.230.21:8000/jmdp?jm=${encodeURIComponent(tup)}`;
              let res = await fetch(url);
              if (!res || !res.ok) {
                logger.error('[jm] 请求失败');
                return await this.reply('错误，请检查车号或稍后重试！');
            }
            await downloadAndAutoDelete(url, tup);
              await e.reply(e.friend.sendFile(`././plugins/example/${tup}.pdf`)) 
              await e.reply('ok')
              return true; 
          }else{
            // 处理响应体内容
          let msg = [segment.image(res.url)]; // 返回的是图片
          const forward = [
            '爱护jm，不要爬这么多本子，jm压力大你bot压力也大，西门',
            `https://18comic.vip/photo/${tup}`
        ];
          forward.push(msg);
          const fmsg = await common.makeForwardMsg(e, forward, `album${tup}`);
          await this.reply(fmsg);
    }
          return true; // 返回 true，阻挡消息不再往下
      } catch (err) {
          logger.error(`[jm] 请求失败：${err}`);
          return await this.reply('请求失败，请检查车号或稍后重试！');
      }
          }
  
   }

   async function downloadAndAutoDelete(targetUrl,tup) {
    try {
      // 解析文件名
      const parsedUrl = new URL(targetUrl);
      let filename = `${tup}.pdf` 
      const filePath = path.join('././plugins/example', filename);
  
      // 下载文件（流式写入）
      const response = await axios({
        method: 'get',
        url: targetUrl,
        responseType: 'stream'
      });
  
      // 创建写入流
      const writer = (await fs.open(filePath, 'w')).createWriteStream();
      
      // 管道传输 + Promise 封装
      await new Promise((resolve, reject) => {
        response.data.pipe(writer)
          .on('finish', resolve)
          .on('error', reject);
      });
  
      console.log(`✅ 文件已下载到：${filePath}`);
  
      // 20秒后删除
      setTimeout(async () => {
        try {
          await fs.unlink(filePath);
          console.log(`🗑️ 文件已删除：${filePath}`);
        } catch (err) {
          console.error('删除失败：', err.message);
        }
      }, 20000);
  
    } catch (error) {
      console.error('❌ 操作失败：', error.message);
    }
  }
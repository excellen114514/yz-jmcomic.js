import common from '../../lib/common/common.js'
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
  async Jm(e){
    
    let tup = "";
    for (let m of e.message) {
      tup += m.text;
     }
     tup = tup.replace(/#jm查/g, "").trim();
    let url = `http://127.0.0.1:8000/jmd?jm=${tup}`;
    let res = await fetch(url).catch((err) => logger.error(err));

         //处理url获取失败
         if (!res) {
            logger.error('[comess] 接口请求失败')
            return await this.reply('错误，请反馈！')
        }
        let msg = [segment.image(res.url)];
        await this.reply(msg);

        return true; //返回true，阻挡消息不再往下
  }
}

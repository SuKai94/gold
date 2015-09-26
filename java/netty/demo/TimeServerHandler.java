package sklcc.susu.netty;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelInboundHandlerAdapter;

/**
 * Created by sukai on 15/9/26.
 */
public class TimeServerHandler extends ChannelInboundHandlerAdapter {

    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        // 将msg转为Netty的ByteBuf对象
        ByteBuf buf = (ByteBuf) msg;
        // 获取缓冲区可读的字节数
        byte[] req = new byte[buf.readableBytes()];
        buf.readBytes(req);
        String body = new String(req, "UTF-8");
        System.out.print("Receive Order: " + body);

        String currentTime = "query time".equalsIgnoreCase(body)? new java.util.Date(System.currentTimeMillis()).toString() : "BAD ORDER";
        ByteBuf resp = Unpooled.copiedBuffer(currentTime.getBytes());
        // 发送给客户端
        ctx.write(resp);
    }

    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        // Netty的write不直接将消息写入SocketChannel，而是发送到缓冲区。直至flush方法调用
        ctx.flush();
    }

    public void exceptionCaught(ChannelHandlerContext ctx) throws Exception {
        ctx.close();
    }
}
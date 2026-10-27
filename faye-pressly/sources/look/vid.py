import sys, subprocess; sys.path.insert(0,'look'); from lib import *
mode=sys.argv[1]; out=sys.argv[2]
W,H,FPS,DUR=1080,1920,30,15
L1=text_layer(W,H,['my kind of','ambitious founder','wants everyone','to rise.'],104,700,lh=1.02,track=-0.035)
L2=text_layer(W,H,['including herself.'],104,1150,track=-0.035)
src=subprocess.Popen(['ffmpeg','-v','error','-t',str(DUR),'-i','/mnt/user-data/uploads/IMG_6487.mov','-vf',f'scale={W}:{H},fps={FPS}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-f','lavfi','-t',str(DUR),'-i','anullsrc=r=44100:cl=stereo','-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-shortest','-movflags','+faststart',out],stdin=subprocess.PIPE)
def ramp(t,a,d=0.35): return float(np.clip((t-a)/d,0,1))
for i in range(DUR*FPS):
    t=i/FPS; f=np.frombuffer(src.stdout.read(W*H*3),np.uint8).reshape(H,W,3).astype(float)
    b=y2k(plum_grade(f,0.78),sat=1.12,bloom=0.35,soft=0.9,grain=7,seed=i%7)
    a1=L1*ramp(t,0.5); a2=L2*ramp(t,8.4)
    if a1.max()>0: b=put_text(b,a1,'#F4EFE6',glow='#F2B3A8' if mode=='D' else '#D9C6F2',glow_r=18,glow_a=0.42)
    if a2.max()>0:
        if mode=='B': b=put_text(b,a2,None,glow='#C9AEF2',glow_r=22,glow_a=0.85,iri=True,t=t*0.25)
        elif mode=='A': b=put_text(b,a2,'#E6D4F8',glow='#B996F0',glow_r=22,glow_a=0.85)
        else: b=put_text(b,a2,'#F7A699',glow='#E86E62',glow_r=22,glow_a=0.85)
        b=stars(b,L2,3,int(t*2)+3,t)
    if t>DUR-0.7: b=b*(1-(t-(DUR-0.7))/0.7)
    enc.stdin.write(np.clip(b,0,255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()

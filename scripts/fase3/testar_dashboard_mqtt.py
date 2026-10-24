"""Confiro o painel real por MQTT em um namespace de ensaio isolado."""
import argparse
import json
from pathlib import Path
import threading
import time
import urllib.request
import uuid

import paho.mqtt.client as mqtt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--topico', required=True)
    parser.add_argument('--url', default='http://127.0.0.1:1881')
    parser.add_argument('--saida', type=Path, required=True)
    parser.add_argument('--pausa-alerta', type=float, default=0)
    args = parser.parse_args()
    if '/dashboard-test/' not in args.topico:
        parser.error('Uso somente namespace dashboard-test para este ensaio.')
    args.saida.mkdir(parents=True, exist_ok=True)
    connected = threading.Event()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='aura-ui-test-'+uuid.uuid4().hex[:10])
    client.on_connect = lambda c,u,f,rc,p: connected.set() if rc == 0 else None
    client.connect_async('broker.hivemq.com',1883)
    client.loop_start()
    assert connected.wait(20), 'Nao consegui conectar o publicador de teste.'
    sid = uuid.uuid4().hex[:16]
    prefix = args.topico+'/devices/cardioia-esp32-01/'

    def state():
        with urllib.request.urlopen(args.url+'/cardioia/api/state',timeout=5) as response:
            return json.load(response)

    def check(name, predicate):
        deadline = time.monotonic()+12
        while True:
            view = state()
            if predicate(view):
                (args.saida/(name+'.json')).write_text(json.dumps(view,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                print('PASS '+name,flush=True)
                return view
            assert time.monotonic()<deadline, (name,view.get('mode'),view.get('alerts'),view.get('lastSequence'))
            time.sleep(.2)

    def publish(kind,data):
        info=client.publish(prefix+kind,json.dumps(data),qos=1,retain=False)
        info.wait_for_publish(8)

    def packet(seq, **changes):
        data=dict(schema_version=1,device_id='cardioia-esp32-01',session_id=sid,sequence=seq,
                  collected_uptime_ms=seq*5000,window_ms=5000,temperature_c=24,humidity_pct=40,
                  pulse_count=6,heart_rate_bpm=72,dht_valid=True,dropped_total=0,backlog_samples=1,
                  simulated=True,transport='mqtt',sent_uptime_ms=seq*5000,age_ms=0,attempt=1,replay=False)
        data.update(changes)
        return data

    try:
        publish('status',dict(device_id='cardioia-esp32-01',session_id=sid,simulated=True,state='online'))
        publish('telemetry',packet(1))
        check('01_atual',lambda v:v.get('session')==sid and v.get('mode')=='live' and not v['alerts'])
        publish('telemetry',packet(1,attempt=2))
        check('02_reenvio',lambda v:v.get('duplicates',0)>0 and len(v['history'])==1)
        publish('telemetry',packet(2,heart_rate_bpm=99))
        check('03_invalida',lambda v:v.get('rejected',0)>0 and v['lastSequence']==1)
        publish('telemetry',packet(2,pulse_count=11,heart_rate_bpm=132,temperature_c=31))
        check('04_primeiro_limiar',lambda v:v.get('lastSequence')==2 and v['pending'] and not v['alerts'])
        publish('telemetry',packet(3,pulse_count=11,heart_rate_bpm=132,temperature_c=31))
        check('05_alerta_confirmado',lambda v:v.get('lastSequence')==3 and len(v['alerts'])==2)
        if args.pausa_alerta:
            deadline=time.monotonic()+args.pausa_alerta
            while time.monotonic()<deadline:
                # Reenvio a mesma identidade sem criar outra janela nem outro episódio.
                publish('telemetry',packet(3,pulse_count=11,heart_rate_bpm=132,temperature_c=31,attempt=2))
                time.sleep(2)
        publish('telemetry',packet(4,pulse_count=10,heart_rate_bpm=120,temperature_c=29))
        check('06_permanencia',lambda v:v.get('lastSequence')==4 and len(v['alerts'])==2 and len([e for e in v['events'] if e['kind']=='alert'])==2)
        publish('telemetry',packet(5,pulse_count=20,heart_rate_bpm=240,temperature_c=50,sent_uptime_ms=85000,age_ms=60000,replay=True,backlog_samples=3))
        check('07_recuperada',lambda v:v.get('lastSequence')==5 and v['mode']=='recovering' and v['current'] is None and not v['alerts'])
        publish('telemetry',packet(6))
        publish('telemetry',packet(7))
        check('08_saida_alerta',lambda v:v.get('lastSequence')==7 and not v['alerts'] and len([e for e in v['events'] if e['kind']=='resolved'])==2)
        publish('telemetry',packet(8,temperature_c=None,humidity_pct=None,dht_valid=False))
        check('09_sensor_indisponivel',lambda v:v.get('lastSequence')==8 and v['current']['temperature_c'] is None and not v['tempKnown'])
        publish('status',dict(device_id='cardioia-esp32-01',session_id=sid,simulated=True,state='offline_simulated'))
        check('10_offline',lambda v:v.get('mode')=='offline' and v['current'] is None)
        publish('status',dict(device_id='cardioia-esp32-01',session_id=sid,simulated=True,state='online'))
        publish('telemetry',packet(9))
        check('11_reconectado',lambda v:v.get('mode')=='live' and v.get('lastSequence')==9)
        time.sleep(16)
        check('12_sem_dados_recentes',lambda v:v.get('mode')=='stale' and v['current'] is None and len(v['history'])==9)
        result={'resultado':'aprovado','origem':'publicador Python de ensaio, sem ESP32','topico':args.topico,'session_id':sid,'cenarios':12}
        (args.saida/'resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    finally:
        client.disconnect()
        client.loop_stop()


if __name__=='__main__':
    main()

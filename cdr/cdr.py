from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import dialects
from sqlalchemy import null
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import union
from sqlalchemy import join
from sqlalchemy import sql
from sqlalchemy import outerjoin
from datetime import datetime
from cdr.tables import QueueLogForExcel
from cdr.tables import CDRViewer
from cdr.datasets import Cdr
from cdr.config import Config


class DBCdr():
    def __init__(self, mysql_user='root', mysql_password='', 
                 mysql_address='127.0.0.1', mysql_port='3306',
                 domain='', dir_record=''):
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_address = mysql_address
        self.mysql_port = mysql_port
        self.domain = domain
        self.dir_record = str(dir_record)
        self.engine = create_engine(
                u"mysql+pymysql://{}:{}@{}/asteriskcdrdb".format(self.mysql_user,
                    self.mysql_password, self.mysql_address), echo=True)

    def change_file_url(self, record_file_name=''):
        if record_file_name is not None:
            del_path_file_name = record_file_name.replace(self.dir_record, '', 1)
            url_file_name = f"{self.domain}{del_path_file_name}"
            return(url_file_name)
        else:
            return(None)

    def get_cdrs(self, start_date: datetime, stop_date: datetime, limit=500, offset=0):
        conn = self.engine.connect()
        stmnt_queuelog = select([QueueLogForExcel.time.label('calldate'),
                                sql.expression.literal_column("\'in\'", String).\
                                    label('direction'),
                                QueueLogForExcel.CLID_Client.label('src'),
                                QueueLogForExcel.DID.label('dst'),
                                QueueLogForExcel.Wait_Time.label('wait_time'),
                                QueueLogForExcel.billsec.label('billsec'),
                                CDRViewer.recordingfile,
                                QueueLogForExcel.agent.label('LineDescription')]).select_from(
                                    join(QueueLogForExcel, CDRViewer, 
                                         and_(
                                              QueueLogForExcel.callid == CDRViewer.linkedid,
                                              QueueLogForExcel.agent == CDRViewer.realdst
                                              ),
                                              isouter=True)).\
                                    where(and_(QueueLogForExcel.time >= start_date,
                                        QueueLogForExcel.time <= stop_date))
        dst_channel_pattern = "|".join(Config.dst_channels)
        stmnt_cdr = select([CDRViewer.calldate.label('calldate'),
                            sql.expression.literal_column("\'out\'", String).\
                                label('direction'),
                            CDRViewer.did.label('src'),
                            CDRViewer.realdst.label('dst'),
                            CDRViewer.duration.op('-')(CDRViewer.billsec).\
                                label('wait_time'),
                            CDRViewer.billsec.label('billsec'),
                            CDRViewer.recordingfile,
                            CDRViewer.src.label('LineDescription')]).\
                                where(
                                    and_(
                                        CDRViewer.calldate >= start_date, 
                                        CDRViewer.calldate <= stop_date,
                                        CDRViewer.dstchannel.\
                                            op('REGEXP')(dst_channel_pattern)
                                        )
                                      )
        select_union = union(stmnt_queuelog, stmnt_cdr).\
                           limit(limit).offset(int(offset))
        results = conn.execute(select_union).fetchall()
        conn.close()
        list_cdr = []
        for db_cdr in results:
            list_cdr.append(Cdr(db_cdr[0], db_cdr[1], db_cdr[2], 
                            db_cdr[3], int(db_cdr[4]), int(db_cdr[5]), 
                            self.change_file_url(record_file_name=db_cdr[6]),
                            db_cdr[7]).__dict__
                           )
        return list_cdr


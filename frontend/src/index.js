import React from 'react';
import ReactDOM from 'react-dom/client';
import 'antd/dist/reset.css';
import { Layout, Input, Button, List, Card } from 'antd';
import axios from 'axios';

const { Header, Content } = Layout;

function App(){
  const [q, setQ] = React.useState('');
  const [res, setRes] = React.useState(null);
  const run = async ()=>{
    const r = await axios.post('/query', {question: q});
    setRes(r.data);
  }
  return (
    <Layout>
      <Header style={{color:'#fff'}}>PoC RAG Demo</Header>
      <Content style={{padding:20}}>
        <Input.Search placeholder='输入问题...' enterButton='查询' onSearch={(v)=>{setQ(v); run();}} />
        {res && (
          <Card style={{marginTop:20}} title='Answer'>
            <div>{res.answer}</div>
            <List dataSource={res.sources} renderItem={item=> (<List.Item>{item.text}</List.Item>)} />
          </Card>
        )}
      </Content>
    </Layout>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

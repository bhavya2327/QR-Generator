import React from 'react';
import { renderToString } from 'react-dom/server';

function CardContent({ profile }) {
    if (!profile) return React.createElement("div", null, "Loading...");
    
    return React.createElement("div", { style: { minHeight: '100vh', backgroundColor: '#f0f2f5', paddingBottom: '2rem' } },
        React.createElement("div", { 
            style: { 
                height: '200px', 
                background: profile.bg && profile.bg.startsWith('http') 
                    ? `url('${profile.bg}') center/cover no-repeat` 
                    : (profile.bg && profile.bg.startsWith('#') ? profile.bg : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
                position: 'relative'
            }
        })
    );
}

const profile = {
  firstName: 'John',
  lastName: 'Doe',
  phone: '+1234567890',
  email: 'john@example.com',
  company: 'Acme Corp',
  desc: 'Software Engineer',
  website: 'https://acme.com',
  linkedin: 'https://linkedin.com/in/johndoe',
  facebook: 'https://facebook.com/johndoe',
  instagram: 'https://instagram.com/johndoe',
  youtube: 'https://youtube.com/johndoe',
  whatsapp: '1234567890',
  photo: 'https://lh3.googleusercontent.com/d/1XhAzsCNTPQUp2m3uuPTvzdzuTeTXPLi9',
  bg: 'https://lh3.googleusercontent.com/d/1R1jHOI4n2gvLt_HnepCJqfKHK4TdFPC-',
  job: ''
};

console.log(renderToString(React.createElement(CardContent, { profile })));

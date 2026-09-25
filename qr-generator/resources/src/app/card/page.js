'use client';
import React, { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import 'bootstrap/dist/css/bootstrap.min.css';

function CardContent() {
    const searchParams = useSearchParams();
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        const dataParam = searchParams.get('data');
        if (dataParam) {
            try {
                const decoded = JSON.parse(decodeURIComponent(atob(dataParam)));
                setProfile(decoded);
            } catch (e) {
                console.error("Failed to parse card data", e);
            }
        }
    }, [searchParams]);

    if (!profile) {
        return (
            <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    const downloadVCard = () => {
        const getSocial = (type, val) => val ? `X-SOCIALPROFILE;type=${type}:${val}\n` : '';
        const website = profile.website ? `URL:${profile.website}\n` : '';
        const photo = profile.photo ? `\nPHOTO;VALUE=URI:${profile.photo}` : '';
        
        const vcard = `BEGIN:VCARD
VERSION:3.0
N:${profile.lastName || ''};${profile.firstName || ''}
FN:${profile.firstName || ''} ${profile.lastName || ''}
ORG:${profile.company || ''}
TITLE:${profile.job || ''}
NOTE:${profile.desc || ''}${photo}
TEL;TYPE=work,voice:${profile.phone || ''}
EMAIL:${profile.email || ''}
${website}${getSocial('linkedin', profile.linkedin)}${getSocial('instagram', profile.instagram)}${getSocial('facebook', profile.facebook)}${getSocial('youtube', profile.youtube)}END:VCARD`;
        
        const blob = new Blob([vcard], { type: 'text/vcard' });
        const file = new File([blob], `${profile.firstName || 'contact'}.vcf`, { type: 'text/vcard' });

        // iPhone/iPad: hand the vCard to the native share sheet (requires HTTPS).
        if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
            navigator.share({
                files: [file],
                title: profile.firstName + " " + profile.lastName,
                text: "Save " + profile.firstName + " " + profile.lastName + " to your contacts"
            }).catch(() => { });
            return;
        }

        // Fallback 1: iOS HTTP fallback (data URI opens directly in Contacts app)
        const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
        if (isIOS) {
            window.location.href = 'data:text/vcard;charset=utf-8,' + encodeURIComponent(vcard);
            return;
        }

        // Fallback 2: Standard Blob download (Desktop, Android HTTP)
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${profile.firstName || 'contact'}.vcf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setTimeout(() => URL.revokeObjectURL(url), 100);
    };

    return (
        <div style={{ minHeight: '100vh', backgroundColor: '#f0f2f5', paddingBottom: '2rem' }}>
            {/* Banner */}
            <div style={{ 
                height: '200px', 
                background: profile.bg && profile.bg.startsWith('http') 
                    ? `url('${profile.bg}') center/cover no-repeat` 
                    : (profile.bg && profile.bg.startsWith('#') ? profile.bg : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
                position: 'relative'
            }}></div>
            
            <div className="container" style={{ maxWidth: '480px', marginTop: '-80px', position: 'relative', zIndex: 10 }}>
                <div className="card shadow-lg border-0 rounded-4 overflow-hidden text-center bg-white">
                    <div className="card-body p-4">
                        {/* Profile Photo */}
                        <div className="mb-3">
                            {profile.photo ? (
                                <img 
                                    src={profile.photo} 
                                    alt="Profile" 
                                    style={{ width: '150px', height: '150px', objectFit: 'cover', borderRadius: '50%', border: '5px solid #fff', boxShadow: '0 4px 10px rgba(0,0,0,0.1)' }} 
                                />
                            ) : (
                                <div 
                                    className="d-inline-flex justify-content-center align-items-center bg-light text-primary"
                                    style={{ width: '150px', height: '150px', borderRadius: '50%', border: '5px solid #fff', boxShadow: '0 4px 10px rgba(0,0,0,0.1)', fontSize: '4rem', fontWeight: 'bold' }}
                                >
                                    {(profile.firstName?.[0] || '')}{(profile.lastName?.[0] || '')}
                                </div>
                            )}
                        </div>
                        
                        {/* Info */}
                        <h2 className="font-weight-bold mb-1" style={{ color: '#1a1a1a' }}>{profile.firstName} {profile.lastName}</h2>
                        <h5 className="text-muted mb-2">{profile.job}</h5>
                        {profile.company && <p className="font-weight-bold text-primary mb-3">{profile.company}</p>}
                        
                        {profile.desc && (
                            <p className="text-muted px-3" style={{ fontSize: '0.95rem' }}>{profile.desc}</p>
                        )}
                        
                        {/* Action Button */}
                        <button onClick={downloadVCard} className="btn btn-primary btn-lg w-100 rounded-pill shadow-sm mt-3 mb-4 fw-bold" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', border: 'none' }}>
                            <i className="fas fa-address-book me-2"></i> Save to Contacts
                        </button>
                        
                        {/* Contact & Social Links */}
                        <div className="text-start mt-4">
                            <h6 className="text-uppercase text-muted fw-bold mb-3" style={{ fontSize: '0.8rem', letterSpacing: '1px' }}>Contact Information</h6>
                            
                            <div className="d-flex flex-column gap-3">
                                {profile.phone && (
                                    <a href={`tel:${profile.phone}`} className="text-decoration-none text-dark d-flex align-items-center p-3 rounded-3" style={{ backgroundColor: '#f8f9fa' }}>
                                        <div className="bg-white rounded-circle d-flex justify-content-center align-items-center shadow-sm" style={{ width: '40px', height: '40px' }}>
                                            <i className="fas fa-phone text-primary"></i>
                                        </div>
                                        <span className="ms-3 fw-medium">{profile.phone}</span>
                                    </a>
                                )}
                                
                                {profile.email && (
                                    <a href={`mailto:${profile.email}`} className="text-decoration-none text-dark d-flex align-items-center p-3 rounded-3" style={{ backgroundColor: '#f8f9fa' }}>
                                        <div className="bg-white rounded-circle d-flex justify-content-center align-items-center shadow-sm" style={{ width: '40px', height: '40px' }}>
                                            <i className="fas fa-envelope text-primary"></i>
                                        </div>
                                        <span className="ms-3 fw-medium">{profile.email}</span>
                                    </a>
                                )}
                                
                                {profile.website && (
                                    <a href={profile.website} target="_blank" rel="noopener noreferrer" className="text-decoration-none text-dark d-flex align-items-center p-3 rounded-3" style={{ backgroundColor: '#f8f9fa' }}>
                                        <div className="bg-white rounded-circle d-flex justify-content-center align-items-center shadow-sm" style={{ width: '40px', height: '40px' }}>
                                            <i className="fas fa-globe text-primary"></i>
                                        </div>
                                        <span className="ms-3 fw-medium text-truncate">Website</span>
                                    </a>
                                )}
                                
                                {/* Social Grid */}
                                <div className="d-flex justify-content-center gap-3 mt-3">
                                    {profile.linkedin && (
                                        <a href={profile.linkedin} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
                                            <div className="rounded-circle d-flex justify-content-center align-items-center shadow-sm text-white" style={{ width: '50px', height: '50px', backgroundColor: '#0077b5' }}>
                                                <i className="fab fa-linkedin-in fs-5"></i>
                                            </div>
                                        </a>
                                    )}
                                    {profile.instagram && (
                                        <a href={profile.instagram} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
                                            <div className="rounded-circle d-flex justify-content-center align-items-center shadow-sm text-white" style={{ width: '50px', height: '50px', background: 'radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%)' }}>
                                                <i className="fab fa-instagram fs-5"></i>
                                            </div>
                                        </a>
                                    )}
                                    {profile.facebook && (
                                        <a href={profile.facebook} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
                                            <div className="rounded-circle d-flex justify-content-center align-items-center shadow-sm text-white" style={{ width: '50px', height: '50px', backgroundColor: '#1877f2' }}>
                                                <i className="fab fa-facebook-f fs-5"></i>
                                            </div>
                                        </a>
                                    )}
                                    {profile.youtube && (
                                        <a href={profile.youtube} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
                                            <div className="rounded-circle d-flex justify-content-center align-items-center shadow-sm text-white" style={{ width: '50px', height: '50px', backgroundColor: '#ff0000' }}>
                                                <i className="fab fa-youtube fs-5"></i>
                                            </div>
                                        </a>
                                    )}
                                    {profile.whatsapp && (
                                        <a href={`https://wa.me/${profile.whatsapp.replace(/[^0-9]/g, '')}`} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
                                            <div className="rounded-circle d-flex justify-content-center align-items-center shadow-sm text-white" style={{ width: '50px', height: '50px', backgroundColor: '#25D366' }}>
                                                <i className="fab fa-whatsapp fs-5"></i>
                                            </div>
                                        </a>
                                    )}
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
                <div className="text-center mt-4 mb-3">
                    <small className="text-muted">Created with <strong>QR Generator</strong></small>
                </div>
            </div>
        </div>
    );
}

export default function CardPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <CardContent />
        </Suspense>
    );
}

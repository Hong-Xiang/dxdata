II=textread('2.txt');
number_block=72;%棱数
number_binX=8; %每条棱上晶体数
number_binY=32;

def crystal(number_binX, number_binY, number_block):
    ID1=fix(crystal1_id/number_binX)*number_binX*number_block+mod(crystal1_id,number_binX)+II(:,1)*number_binX
    ID2=fix(crystal2_id/number_binX)*number_binX*number_block+mod(crystal2_id,number_binX)+II(:,3)*number_binX
    return ID1, ID2

# system with 8 blocks
crystal(10, 10, 8)


clc;
clear;
close all;
IV=textread('\\192.168.1.114\share\ring3-3-20.txt');
1
%% 坐标转crystal编号
number_block=16;%棱数
number_binX=10;%每条棱上晶体数
number_binY=10;%轴向层数
R_inner=97; %圆环内半径
thickness=20;%晶体厚度
len_block=33.6;%block边长
len_crystal=len_block/number_binX;
L=33.6;%轴向长度mm
% R_FOV=442;%FOV半径mm
nDetectors=number_block*number_binX;%单环上晶体个数
%M=nDetectors/2;N=nDetectors/2;
layer=number_binY;
% SINO=zeros(M+2,N+2,layer*layer);
% crystal1=int32(zeros(size(IV,1)/2,1));
% crystal2=int32(zeros(size(IV,1)/2,1));
% ring1IDD=int32(zeros(size(IV,1)/2,1));
% ring2IDD=int32(zeros(size(IV,1)/2,1));
parfor i=1:size(IV,1)
    theta=acosd(dot(IV(i,1:2),[1,0])/(norm(IV(i,1:2))));
    if IV(i,2)<0
        theta=360-theta;
    end
    theta=theta+180/nDetectors*number_binX;
    if theta>=360
        theta=theta-360;
    end
    block=floor(theta/360*number_block);
    center=R_inner*[cos(2*block*pi/number_block),sin(2*block*pi/number_block)];
    vec1=center/R_inner;       %block平面的法向量
    vec=[-sin(2*block*pi/number_block),cos(2*block*pi/number_block)];  %block平面内的向量
    pro_point= dot(center-IV(i,1:2),vec1)*vec1+IV(i,1:2);
    edge_block=center-vec*len_block/2;
    crystal=floor(norm(pro_point-edge_block)/len_crystal);
%     ring=floor((IV(i,3)+L/2)/L*layer);
    num_crystal(i,:)=[block,crystal];    
end

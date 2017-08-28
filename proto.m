% given a random quality and similarity matrix, select the k best documents
m = 10; % the number of hypothetical documents
k = 5; % the number we'll be selecting
q = rand(m,1); % the dummy quality matrix, m quality vectors of length 5
S = rand(m); % the dummy similarity matrix

for i = 1 : m
    S(i,i) = 0;
end

b = 665; % the standard by DUC

L = S .* (q*q'); %Lij = qi*qj*Sij       
L = 0.5*(L+L');
[V, Lam] = eig(full(L));
Lam(Lam<0) = 0;
L = V*Lam*V';    % project L into the PSD cone

flag = true(m,1); % initialize all elements to be valid candidates
%flag(sum(doc.txt>0,2) < min_words) = false; % There is no need to filter
%by sentence lenth for now


Y = []; % initialize y to be empty
val_old = 0; % initialize the old value of det(Ly) to 0
%while any(flag) % so long as any valid candidates remain
for t = 1 : k
    inds = find(flag); % create a vector containing their indices
    p = zeros(size(inds)); % and initialize a vector of zeroes of the same length
    for iter = 1 : length(inds) % for each valid candidate
        i = inds(iter); % take its index
        Ytmp = [i; Y]; % and add it to the top of Ytmp
        p(iter) = (det(L(Ytmp,Ytmp)) - val_old); % then the corresponding value of p to det(Lytmp) - det(Ly)
    end
    [val, pos] = max(p); % take the max of p
     %if val < val_old
        %break;
     %end
    Y = [inds(pos); Y]; % and add its corresponding index of flags to Y
    val_old = det(L(Y,Y)); % update det(Ly)
    %lenY = sum(doc.cost(Y));
    flag(Y) = false; % remove the candidate just selected from the list of candidates
    %flag(doc.cost > b - lenY) = false;
end

 Y=flip(Y); %reverse the order of Y, so the first candidate selected is on top
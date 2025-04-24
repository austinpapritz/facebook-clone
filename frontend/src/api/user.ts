import API from './client';

export const getUser = async (id: number) => {
  const res = await API.get(`/users/${id}`);
  return res.data;
};